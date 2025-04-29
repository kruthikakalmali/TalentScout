import React from "react";
import {
  Box,
  Flex,
  Text,
  Button,
  Icon,
  VStack,
  useColorModeValue,
} from "@chakra-ui/react";
import { CheckCircleIcon } from "@chakra-ui/icons";

interface InterviewCompleteProps {
  sessionId: string;
  bigAudioUrl: string | null;
  onGenerateReport: () => void;
}

const InterviewComplete: React.FC<InterviewCompleteProps> = ({
  sessionId,
  bigAudioUrl,
  onGenerateReport,
}) => {
  const cardBg = useColorModeValue("gray.700", "gray.800");
  const subtitleColor = useColorModeValue("gray.300", "gray.400");
  const audioBg = useColorModeValue("gray.600", "gray.700");

  return (
    <Box
      w="70%"
      bg={cardBg}
      p={8}
      borderRadius="2xl"
      boxShadow="xl"
      textAlign="center"
      mx="auto"
    >
        <Flex align="center" justify="center" mb={4} mt={200}>
          <Icon as={CheckCircleIcon} boxSize={10} color="green.400" mr={2} />
          <Text fontSize="3xl" fontWeight="extrabold" color="white">
            Interview Complete!
          </Text>
        </Flex>

        <Text fontSize="md" color={subtitleColor} mb={6}>
          Thanks for finishing your session. Click below to generate your
          detailed feedback report.
        </Text>

        <Button
          size="lg"
          colorScheme="purple"
          mb={6}
          onClick={onGenerateReport}
        >
          Generate Report
        </Button>

      {bigAudioUrl ? (
        <VStack spacing={3} p={4} bg={audioBg} borderRadius="md">
          <Text fontWeight="semibold" color="white">
            Session Recording
          </Text>
          <Box w="100%">
            <audio controls src={bigAudioUrl} style={{ width: "100%" }} />
          </Box>
        </VStack>
      ) : (
        <Text color={subtitleColor}>Preparing your recording…</Text>
      )}
    </Box>
  );
};

export default InterviewComplete;
