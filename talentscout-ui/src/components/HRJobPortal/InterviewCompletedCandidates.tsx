import React, { useEffect, useState } from "react";
import {
  Flex,
  Box,
  Text,
  Button,
  HStack,
  VStack,
  Spacer,
  useColorModeValue,
  useToast,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Header from "../Header";
import Loader from "../Loader";
import { PROD_HOST_URL } from "../../constants";

interface Applicant {
  id: string;
  name: string;
  email: string;
  job_id: string;
  session_id: string;
}

const InterviewCompletedCandidates: React.FC = () => {
  const bgGradient = useColorModeValue(
    "linear(to-br, gray.900, gray.800)",
    "linear(to-br, gray.900, gray.800)"
  );
  const containerBg = useColorModeValue("gray.700", "gray.600");

  const [applicants, setApplicants] = useState<Applicant[]>([]);
  const [loading, setLoading] = useState(false);
  const toast = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    fetchInterviewCompletedApplicants();
  }, []);

  const fetchInterviewCompletedApplicants = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `${PROD_HOST_URL}/get_all_interview_completed_applicants`
      );
      setApplicants(response.data.applications || []);
    } catch (error) {
      console.error(error);
      toast({
        title: "Error fetching completed interviews!",
        status: "error",
        duration: 3000,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateFeedbackReport = (applicant: Applicant) => {
    navigate(
      `/recruiter/generated-feedback-report?session_id=${applicant.session_id}`
    );
  };

  return (
    <Flex
      direction="column"
      h="100vh"
      bgGradient={bgGradient}
      color="whiteAlpha.900"
    >
      <Header title="Completed Interviews" />

      {loading ? (
        <Flex justify="center" align="center" flex="1">
          <Loader />
        </Flex>
      ) : applicants.length === 0 ? (
        <Flex justify="center" align="center" flex="1">
          <Text fontSize="2xl" color="gray.400">
            No completed interviews found.
          </Text>
        </Flex>
      ) : (
        <Flex
          flex="1"
          direction="column"
          maxW="7xl"
          w="full"
          mx="auto"
          justify="space-between"
          p={10}
        >
          <Box
            w="100%"
            flex="1"
            bg="#262934"
            backdropFilter="blur(6px)"
            borderRadius="md"
            boxShadow="md"
            display="flex"
            flexDir="column"
            p={6}
            minH="0"
            transition="all 0.2s"
          >
            <VStack align="stretch" spacing={4} overflowY="auto" flex="1">
              {applicants.map((applicant) => (
                <Box key={applicant.id} p={6} bg={containerBg} borderRadius="2xl">
                  <HStack spacing={4}>
                    <VStack align="start" spacing={1}>
                      <Text fontWeight="bold" fontSize="xl">{applicant.name}</Text>
                      <Text fontSize="sm" color="gray.300">Email: {applicant.email}</Text>
                      <Text fontSize="sm" color="gray.300">Job ID: {applicant.job_id}</Text>
                    </VStack>
                    <Spacer />
                    <HStack spacing={3}>
                      <Button
                        size="md"
                        colorScheme="purple"
                        onClick={() => handleGenerateFeedbackReport(applicant)}
                      >
                        Generate Feedback Report
                      </Button>
                    </HStack>
                  </HStack>
                </Box>
              ))}
            </VStack>
          </Box>
        </Flex>
      )}
    </Flex>
  );
};

export default React.memo(InterviewCompletedCandidates);
