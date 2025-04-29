import { useState, useRef, useEffect } from "react";

interface UseAudioRecorderOptions {
  withTranscription?: boolean;
  uploadUrl?: string;
  fileName?: string;
  autoStart?: boolean;
}

export const useAudioRecorder = ({
  withTranscription = false,
  uploadUrl,
  fileName,
  autoStart = false,
}: UseAudioRecorderOptions) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [elapsed, setElapsed] = useState(0);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const recognitionRef = useRef<any>(null);
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    if (autoStart) startRecording();
    return () => {
      recognitionRef.current?.stop?.();
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
        mediaRecorderRef.current.stream.getTracks().forEach((t) => t.stop());
      }
      if (timerRef.current != null) clearInterval(timerRef.current);
    };
  }, [autoStart]);

  const convertSpeechToText = () => {
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) return;
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";
    recognition.onresult = (event: SpeechRecognitionEvent) => {
      let finalText = "", interimText = "";
      for (let i = 0; i < event.results.length; i++) {
        const result = event.results[i];
        const text = result[0].transcript;
        if (result.isFinal) finalText += text + " ";
        else interimText += text;
      }
      setTranscript((finalText + interimText).trim());
    };
    recognition.onerror = (e: any) => console.error("SpeechRecognition error", e);
    recognition.start();
    recognitionRef.current = recognition;
  };

  const startRecording = async () => {
    setTranscript("");
    setElapsed(0);
    if (withTranscription) convertSpeechToText();
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      audioChunksRef.current = [];
      recorder.ondataavailable = (e: BlobEvent) => audioChunksRef.current.push(e.data);
      recorder.start();
      mediaRecorderRef.current = recorder;
      setIsRecording(true);
    } catch (error) {
      console.error("MediaRecorder error", error);
    }
  };

  const stopRecording = async (): Promise<Blob | null> => {
    recognitionRef.current?.stop?.();
    if (!mediaRecorderRef.current) return null;
    const recorder = mediaRecorderRef.current;
    await new Promise<void>((resolve) => {
      recorder.onstop = () => resolve();
      recorder.stop();
    });
    recorder.stream.getTracks().forEach((t) => t.stop());
    if (timerRef.current != null) clearInterval(timerRef.current);
    setIsRecording(false);

    const blob = new Blob(audioChunksRef.current, { type: recorder.mimeType || "audio/webm" });
    const url = URL.createObjectURL(blob);
    setAudioUrl(url);

    if (uploadUrl && fileName) {
      const sessionId = sessionStorage.getItem("session_id") || "";
      const formData = new FormData();
      formData.append("session_id", sessionId);
      formData.append("audio_file", blob, fileName);
      try {
        await fetch(uploadUrl, { method: "POST", body: formData });
      } catch (err) {
        console.error("Upload error", err);
      }
    }
    return blob;
  };

  return {
    isRecording,
    transcript,
    elapsed,
    audioUrl,
    startRecording,
    stopRecording,
  };
};