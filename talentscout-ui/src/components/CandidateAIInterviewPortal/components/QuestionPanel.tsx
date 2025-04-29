// src/components/QuestionPanel.tsx

import React, { useRef, useEffect, useState } from "react";
import axios from "axios";
import { Box, Flex, Text, Button } from "@chakra-ui/react";
import QuestionBox from "./QuestionBox";
import RecordButton from "./RecordButton";
import InterviewComplete from "./InterviewComplete";
import { useAudioRecorder } from "./useAudioRecorder";
import { PROD_HOST_URL } from "../../../constants";
import { useNavigate } from "react-router-dom";

interface QuestionPanelProps {
  sessionId: string;
  currentQuestion: string;
  setCurrentQuestion: React.Dispatch<React.SetStateAction<string | null>>;
  onClipRecorded: (clip: {
    url: string;
    transcript: string;
    question: string;
  }) => void;
  onQuestionAnswered: () => void;
  interviewEnded: boolean;
  onInterviewComplete: (audioUrl: string) => void;
}

const QuestionPanel: React.FC<QuestionPanelProps> = ({
  sessionId,
  currentQuestion,
  setCurrentQuestion,
  onClipRecorded,
  onQuestionAnswered,
  interviewEnded,
  onInterviewComplete,
}) => {
  const small = useAudioRecorder({ withTranscription: true });
  const session = useAudioRecorder({
    uploadUrl: `${PROD_HOST_URL}/upload`,
    fileName: `${sessionId}.mp3`,
  });
  const sessionStarted = useRef(false);
  const [bigAudioUrl, setBigAudioUrl] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleRecordClick = async () => {
    if (small.isRecording) {
      const blob = (await small.stopRecording())!;
      const url = URL.createObjectURL(blob);
      const transcript = small.transcript;

      try {
        const resp = await axios.post(
          `${PROD_HOST_URL}/submit_adaptive_response`,
          { session_id: sessionId, transcript }
        );
        const nextQuestion = resp.data.next_question || "";
        onClipRecorded({ url, transcript, question: currentQuestion });
        setCurrentQuestion(nextQuestion);
        onQuestionAnswered();
      } catch (err) {
        console.error("Transcript API error", err);
      }
    } else {
      small.startRecording();
      if (!sessionStarted.current) {
        session.startRecording();
        sessionStarted.current = true;
      }
    }
  };

  // When interview ends, finalize the big‐session, upload & expose URL
  useEffect(() => {
    if (!interviewEnded || !sessionStarted.current) return;
    (async () => {
      const blob = await session.stopRecording();
      if (!blob) return;
      const form = new FormData();
      form.append("session_id", sessionId);
      form.append("audio_file", blob, `${sessionId}.mp3`);
      try {
        await axios.post(`${PROD_HOST_URL}/upload`, form);
      } catch (err) {
        console.error("Full‐session upload error", err);
      }
      const url = URL.createObjectURL(blob);
      setBigAudioUrl(url);
      onInterviewComplete(url);
    })();
  }, [interviewEnded]);

  if (interviewEnded) {
    return (
      <InterviewComplete
        sessionId={sessionId}
        bigAudioUrl={bigAudioUrl}
        onGenerateReport={() => navigate(`/candidate/generated-feedback-report?session_id=${sessionId}`)}
      />
    );
  }

  return (
    <Box
      w="70%"
      h="100%"
      bg="#2d3748"
      p={6}
      display="flex"
      flexDir="column"
      justifyContent="space-between"
      borderRadius="2xl"
    >
      <Box textAlign="center" mt={8}>
        <QuestionBox question={currentQuestion} />
        <Flex justify="center" mt={15}>
          <RecordButton
            onClick={handleRecordClick}
            isRecording={small.isRecording}
          />
        </Flex>
      </Box>

      {small.isRecording && (
        <Box w="100%" mb={4}>
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
            {small.transcript || <i>Listening...</i>}
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default React.memo(QuestionPanel);
