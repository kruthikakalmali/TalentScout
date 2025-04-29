// src/CandidateAIInterviewPortal.tsx

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Flex, Text, Button, useColorModeValue } from "@chakra-ui/react";
import Header from "../Header/Header";
import QuestionPanel from "./components/QuestionPanel";
import QuestionHistory from "./components/QuestionHistory";
import Loader from "../Loader";
import { PROD_HOST_URL } from "../../constants";

const MAX_INTERVIEW_TIME = 30 * 60; 
const MAX_QUESTIONS = 20;

const CandidateAIInterviewPortal: React.FC = () => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const [secondsElapsed, setSecondsElapsed] = useState(0);
  const [questionCount, setQuestionCount] = useState(0);

  // New state
  const [interviewEnded, setInterviewEnded] = useState(false);
  const [clips, setClips] = useState<
    { url: string; transcript: string; question: string }[]
  >([]);

  const bgGradient = useColorModeValue(
    "linear(to-br, gray.900, gray.800)",
    "linear(to-br, gray.900, gray.800)"
  );

  // Global timer
  useEffect(() => {
    if (!sessionId || interviewEnded) return;
    const timer = setInterval(() => {
      setSecondsElapsed((s) => {
        if (s + 1 >= MAX_INTERVIEW_TIME) {
          handleStopInterview();
          return MAX_INTERVIEW_TIME;
        }
        return s + 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [sessionId, interviewEnded]);

  const startSession = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams(window.location.search);
      const job_id = params.get("job_id") || "";
      const identity_id = params.get("identity_id") || "";

      sessionStorage.setItem("job_id", job_id);
      sessionStorage.setItem("identity_id", identity_id);

      const { data } = await axios.post(
        `${PROD_HOST_URL}/start_adaptive_interview`,
        { job_id, identity_id }
      );

      sessionStorage.setItem("session_id", data.session_id);
      setSessionId(data.session_id);
      setCurrentQuestion(data.first_question);
      setQuestionCount(1);
    } catch (err) {
      console.error("Session start error", err);
    } finally {
      setLoading(false);
    }
  };

  // Signal interview end
  const handleStopInterview = () => {
    setInterviewEnded(true);
  };

  const formatTime = (s: number) =>
    `${Math.floor(s / 60)
      .toString()
      .padStart(2, "0")}:${(s % 60).toString().padStart(2, "0")} / ${Math.floor(
      MAX_INTERVIEW_TIME / 60
    ).toString()}:00`;

  return (
    <Flex direction="column" h="100vh" bgGradient={bgGradient} color="whiteAlpha.900">
      <Header title="AI Screening Interview Portal" />

      {!sessionId && !loading && (
        <Flex flex="1" direction="column" justify="center" align="center" p={6} textAlign="center">
          <Text fontSize="xl" mb={6} maxW="600px">
            Welcome to the AI Adaptive Interview Portal! Engage with questions
            tailored to your profile and job description—each one adapting to
            your previous answers. Speak your responses and watch a live
            transcript as you go. Transcripts and audio recordings remain
            available in-app only for the duration of your session. Once the
            interview ends, you’ll receive an email containing a link to view
            your detailed feedback on knowledge, confidence, and communication
            skills.
          </Text>
          <Button size="lg" colorScheme="purple" onClick={startSession}>
            Start Interview
          </Button>
        </Flex>
      )}

      {loading && (
        <Flex flex="1" justify="center" align="center">
          <Loader />
        </Flex>
      )}

      {sessionId && !loading && (
        <>
          {/* Top bar only while live */}
          {!interviewEnded && (
            <Flex justify="space-between" align="center" p={6}>
              <Text>Time: {formatTime(secondsElapsed)}</Text>
              <Text>
                Questions: {questionCount}/{MAX_QUESTIONS}
              </Text>
              <Button size="sm" colorScheme="red" onClick={handleStopInterview}>
                Stop Interview
              </Button>
            </Flex>
          )}

          <Flex flex="1" p={6} gap={4} overflow="hidden">
            <QuestionPanel
              sessionId={sessionId}
              currentQuestion={currentQuestion!}
              setCurrentQuestion={setCurrentQuestion!}
              onClipRecorded={(clip) => setClips((c) => [...c, clip])}
              onQuestionAnswered={() =>
                setQuestionCount((c) => {
                  const next = c + 1;
                  if (next > MAX_QUESTIONS) handleStopInterview();
                  return next;
                })
              }
              interviewEnded={interviewEnded}
              onInterviewComplete={(url) => {
                console.log("Full session audio ready:", url);
              }}
            />

            <QuestionHistory recordings={clips} setClips={setClips} />
          </Flex>
        </>
      )}
    </Flex>
  );
};

export default CandidateAIInterviewPortal;
