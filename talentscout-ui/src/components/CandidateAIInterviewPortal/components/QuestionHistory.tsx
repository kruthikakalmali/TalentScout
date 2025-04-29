import React, { useEffect, useState } from "react";
import {
  Box,
  Text,
  IconButton,
  Tooltip,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Button,
  useColorModeValue,
  Icon,
} from "@chakra-ui/react";
import { FaFileAlt } from "react-icons/fa";

export interface QuestionHistoryObject {
  url: string;
  transcript: string;
  question: string;
}

interface QuestionHistoryProps {
  recordings: QuestionHistoryObject[];
  setClips: React.Dispatch<
    React.SetStateAction<
      {
        url: string;
        transcript: string;
        question: string;
      }[]
    >
  >;
}

const QuestionHistory: React.FC<QuestionHistoryProps> = ({
  recordings,
  setClips,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [currentTranscript, setCurrentTranscript] = useState<string>("");

  const openModal = (transcript: string) => {
    setCurrentTranscript(transcript);
    setIsOpen(true);
  };

  const closeModal = () => {
    setIsOpen(false);
    setCurrentTranscript("");
  };

  const cardBg = useColorModeValue("#2d3748", "#2d3748");
  const textColor = useColorModeValue("whiteAlpha.900", "whiteAlpha.900");
  const modalBg = "#262934";
  const modalColor = "whiteAlpha.900";

  useEffect(() => {
    return () => {
      setClips([]);
    };
  }, []);

  return (
    <Box
      w="30%"
      bg="whiteAlpha.100"
      backdropFilter="blur(8px)"
      borderRadius="2xl"
      boxShadow="md"
      p={6}
      transition="all 0.2s"
      display="flex"
      flexDirection="column"
    >
      <Text
        align="center"
        fontSize="xl"
        fontWeight="semibold"
        color={textColor}
        mb={5}
        flexShrink={0}
      >
        Recordings & Transcripts
      </Text>
      <Box flex="1" overflowY="auto" maxH="77vh">
        {recordings.map((rec, idx) => (
          <Box key={idx} bg={cardBg} borderRadius="md" p={4} mb={4}>
            <Text fontSize="md" fontWeight="medium" color={textColor} mb={2}>
              {`Q${idx + 1}: ${rec.question}`}
            </Text>
            <Box display="flex" alignItems="center">
              <audio controls src={rec.url} style={{ width: "80%" }} />
              <Tooltip label="Show Answer's Transcript" placement="top">
                <IconButton
                  aria-label="Show Transcript"
                  icon={<Icon as={FaFileAlt as any} color="whiteAlpha.900" />}
                  ml={2}
                  onClick={() => openModal(rec.transcript)}
                  colorScheme="teal"
                />
              </Tooltip>
            </Box>
          </Box>
        ))}
      </Box>

      <Modal isOpen={isOpen} onClose={closeModal} size="xl" isCentered>
        <ModalOverlay />
        <ModalContent bg={modalBg} color={modalColor} maxH="80vh">
          <ModalHeader textAlign="center">Answer's Transcript</ModalHeader>
          <ModalCloseButton />
          <ModalBody
            overflowY="auto"
            flex={1}
            maxH="calc(80vh - 120px)"
            whiteSpace="pre-wrap"
            bg={cardBg}
            pl={3}
            pr={3}
            mr={4}
            ml={4}
            borderRadius="lg"
          >
            {currentTranscript || "No transcript available."}
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="purple" onClick={closeModal}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default React.memo(QuestionHistory);
