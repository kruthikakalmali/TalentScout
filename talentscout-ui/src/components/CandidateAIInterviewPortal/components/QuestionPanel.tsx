import React, { useState, useRef, useEffect } from "react";
import {
  Box,
  CircularProgress,
  CircularProgressLabel,
  Flex,
  Text,
  useColorModeValue,
} from "@chakra-ui/react";
import QuestionBox from "./QuestionBox";
import RecordButton from "./RecordButton";

interface QuestionPanelProps {
  question: string;
}

const MAX_RECORD_TIME = 10; // max seconds for recording

const QuestionPanel: React.FC<QuestionPanelProps> = ({ question }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [elapsed, setElapsed] = useState(0);

  const recognitionRef = useRef<any>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<number | null>(null);

  const panelBg = useColorModeValue("whiteAlpha.200", "whiteAlpha.100");
  const trackColor = useColorModeValue("whiteAlpha.300", "blackAlpha.200");

  // timer effect
  useEffect(() => {
    if (isRecording) {
      timerRef.current = window.setInterval(() => {
        setElapsed((prev) => {
          if (prev + 1 >= MAX_RECORD_TIME) {
            stopRecording();
            return MAX_RECORD_TIME;
          }
          return prev + 1;
        });
      }, 1000);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isRecording]);

  const formatTime = (sec: number) => {
    const m = Math.floor(sec / 60)
      .toString()
      .padStart(2, "0");
    const s = (sec % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
  };

  const startRecording = async () => {
    setTranscript("");
    setElapsed(0);

    // SpeechRecognition for live transcript
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recog = new SpeechRecognition();
      recog.continuous = true;
      recog.interimResults = true;
      recog.lang = "en-US";
      recog.onresult = (event: any) => {
        let finalText = "";
        let interimText = "";
        for (let i = 0; i < event.results.length; i++) {
          const res = event.results[i];
          const txt = res[0].transcript;
          if (res.isFinal) finalText += txt + " ";
          else interimText += txt;
        }
        setTranscript((finalText + interimText).trim());
      };
      recog.onerror = (e: any) => console.error("SpeechRecognition error", e);
      recog.start();
      recognitionRef.current = recog;
    }

    // MediaRecorder for audio blob
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      audioChunksRef.current = [];
      recorder.ondataavailable = (e: BlobEvent) => {
        audioChunksRef.current.push(e.data);
      };
      recorder.onstop = () => {
        const blob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        uploadAudio(blob);
      };
      recorder.start();
      mediaRecorderRef.current = recorder;
    } catch (err) {
      console.error("MediaRecorder error", err);
    }

    setIsRecording(true);
  };

  const stopRecording = () => {
    if (recognitionRef.current) recognitionRef.current.stop();
    if (mediaRecorderRef.current) mediaRecorderRef.current.stop();
    if (timerRef.current !== null) {
      clearInterval(timerRef.current);
    }
    setIsRecording(false);
    setElapsed(0)
  };

  const handleRecordClick = () => {
    if (isRecording) stopRecording();
    else startRecording();
  };

  const uploadAudio = async (blob: Blob) => {
    const sessionId = sessionStorage.getItem('session_id') || '';
    const formData = new FormData();
    formData.append('session_id', sessionId);
    formData.append('audio_file', blob, 'recording.mp3');

    try {
      await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
    } catch (err) {
      console.error('Upload error', err);
    }
  };

  return (
    <Box
      w="70%"
      h="100%"
      bg={'#262934'}
      backdropFilter="blur(6px)"
      borderRadius="md"
      boxShadow="md"
      display="flex"
      flexDir="column"
      alignItems="center"
      justifyContent="space-between"
      p={6}
      minH="0"
      transition="all 0.2s"
    >
      <Box textAlign="center" w="100%" mt={20} style={{ marginTop: "200px" }}>
        <Box mb={4} w="80%" mx="auto" mt={20}>
          <QuestionBox question={question} />
        </Box>
        <Flex direction="column" align="center" justify="center">
          <CircularProgress
            value={(elapsed / MAX_RECORD_TIME) * 100}
            size="135px"
            color="teal.300"
            trackColor={trackColor}
            thickness="8px"
          >
            <CircularProgressLabel>
              <Box>
                <RecordButton
                  onClick={handleRecordClick}
                  isRecording={isRecording}
                />
              </Box>
            </CircularProgressLabel>
          </CircularProgress>
          {isRecording && (
            <Text mt={4} fontSize="md" color="whiteAlpha.900">
              {formatTime(elapsed)} / {formatTime(MAX_RECORD_TIME)}
            </Text>
          )}
        </Flex>
      </Box>
      {isRecording && (
        <Box w="90%" mb={4}>
          <Text
            fontSize="lg"
            fontWeight="semibold"
            color="whiteAlpha.900"
            mb={2}
          >
            Live Transcript
          </Text>
          <Box
            w="100%"
            h="200px"
            overflowY="auto"
            bg="whiteAlpha.300"
            p={4}
            borderRadius="sm"
            border="1px solid"
            borderColor="whiteAlpha.400"
            fontSize="md"
            lineHeight="1.4"
          >
            {transcript || <i>Listening...</i>}
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default React.memo(QuestionPanel);
