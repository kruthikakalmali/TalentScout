import React, { useState } from "react";
import {
  Flex,
  Box,
  Text,
  Button,
  Spinner,
  useColorModeValue,
} from "@chakra-ui/react";
import Header from "../Header/Header";
import QuestionPanel from "./components/QuestionPanel";
import QuestionHistory from "./components/QuestionHistory";
import Loader from "../Loader";

const list = [
  {
    question: "some random question?",
    answer:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum dolore sapiente assumenda natus rem illum enim aspernatur voluptatem quaerat at iusto est repellat doloremque, id impedit. Molestiae, consequuntur. Iure, aspernatur. Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum dolore sapiente assumenda natus rem illum enim aspernatur voluptatem quaerat at iusto est repellat doloremque, id impedit. Molestiae, consequuntur. Iure, aspernatur. Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum dolore sapiente assumenda natus rem illum enim aspernatur voluptatem quaerat at iusto est repellat doloremque, id impedit. Molestiae, consequuntur. Iure, aspernatur. Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum dolore sapiente assumenda natus rem illum enim aspernatur voluptatem quaerat at iusto est repellat doloremque, id impedit. Molestiae, consequuntur. Iure, aspernatur. Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum dolore sapiente assumenda natus rem illum enim aspernatur voluptatem quaerat at iusto est repellat doloremque, id impedit. Molestiae, consequuntur. Iure, aspernatur.",
  },
  {
    question: "some random question 2?",
    answer:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum dolore sapiente assumenda natus rem illum enim aspernatur voluptatem quaerat at iusto est repellat doloremque, id impedit. Molestiae, consequuntur. Iure, aspernatur.",
  },
  {
    question: "some random question 2?",
    answer:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum dolore sapiente assumenda natus rem illum enim aspernatur voluptatem quaerat at iusto est repellat doloremque, id impedit. Molestiae, consequuntur. Iure, aspernatur.",
  },
  {
    question: "some random question 2?",
    answer:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Nostrum dolore sapiente assumenda natus rem illum enim aspernatur voluptatem quaerat at iusto est repellat doloremque, id impedit. Molestiae, consequuntur. Iure, aspernatur.",
  },
];

const CandidateAIInterviewPortal: React.FC = () => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const bgGradient = useColorModeValue(
    "linear(to-br, gray.900, gray.800)",
    "linear(to-br, gray.900, gray.800)"
  );

  const startSession = async () => {
    setLoading(true);
    try {
      const res = await fetch("/startSession", { method: "POST" });
      const data = await res.json(); // expected { session_id: string }
      sessionStorage.setItem("session_id", data.session_id);
      setSessionId(data.session_id);
    } catch (err) {
      console.error("Session start error", err);
    } finally {
      // mock API delay
      setTimeout(() => {
        sessionStorage.setItem("session_id", "test");
        setSessionId("test");
        setLoading(false);
      }, 2000);
    }
  };

  return (
    <Flex
      direction="column"
      h="100vh"
      bgGradient={bgGradient}
      color="whiteAlpha.900"
    >
      <Header title="AI Screening Interview Portal" />

      {/* Initial Intro */}
      {!sessionId && !loading && (
        <Flex
          flex="1"
          direction="column"
          justify="center"
          align="center"
          p={6}
          textAlign="center"
        >
          <Text fontSize="2xl" mb={6} maxW="600px">
            Welcome to the AI Mock Interview Portal! Here you’ll receive
            interview questions, record your answers, see a live transcript, and
            get feedback on knowledge, confidence, and communication skills.
          </Text>
          <Button size="lg" colorScheme="purple" onClick={startSession}>
            Start Session
          </Button>
        </Flex>
      )}

      {loading && (
        <Flex flex="1" justify="center" align="center">
          <Loader />
        </Flex>
      )}

      {sessionId && !loading && (
        <Flex flex="1" p={6} gap={4} overflow="hidden">
          <QuestionPanel question="Some random question?" />
          <QuestionHistory questionsList={list} />
        </Flex>
      )}
    </Flex>
  );
};

export default CandidateAIInterviewPortal;
