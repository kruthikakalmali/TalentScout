import React, { useEffect, useState } from "react";
import axios from "axios";
import { useSearchParams } from "react-router-dom";
import {
  Box,
  Flex,
  useColorModeValue,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  VStack,
  Text,
  Divider,
  Spinner,
} from "@chakra-ui/react";
import { PROD_HOST_URL } from "../../constants";
import Header from "../Header";
import { AudioAnalysisScores, OverallTechnicalScore } from "./GenerateReportScores";
import GenerateReportTechnicalAccordian from "./GenerateReportTechnicalAccordian";
import Loader from "../Loader";

interface GenerateReportPageProps {
  reportType: "recruiter" | "candidate";
}

interface ReportResponse {
  report: {
    audio_analysis: {
      confidence_score: number;
      calmness_score: number;
      energy_score: number;
      expressiveness_score: number;
      recruiter_summary?: string;
      candidate_feedback?: {
        positive: string;
        suggestions: string;
      };
    };
    technical_analysis: {
      recruiter_summary?: string;
      candidate_feedback?: {
        positive: string;
        suggestions: string;
      };
      overall_technical_score: number;
      per_question: any[];
    };
  };
}

const GenerateReportPage: React.FC<GenerateReportPageProps> = ({ reportType }) => {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get("session_id") || "";
  const [data, setData] = useState<ReportResponse["report"] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch report when component mounts
  useEffect(() => {
    const fetchReport = async () => {
      if (!sessionId) {
        setError("No session_id provided in query parameters.");
        return;
      }

      setLoading(true);
      try {
        const response = await axios.post<ReportResponse>(
          `${PROD_HOST_URL}/generate_report`,
          { session_id: sessionId }
        );
        setData(response.data.report);
      } catch (err: any) {
        setError(err.message || "Failed to fetch report.");
      } finally {
        setLoading(false);
      }
    };

    fetchReport();
  }, [sessionId]);

  const bgGradient = useColorModeValue(
    "linear(to-br, gray.900, gray.800)",
    "linear(to-br, gray.900, gray.800)"
  );
  const HEADER_TITLE = reportType === "recruiter" ? "Candidate's Feedback" : "Interview Feedback";

  const tabBg = useColorModeValue("gray.700", "gray.800");
  const panelBg = useColorModeValue("gray.800", "gray.700");

  if (loading) {
    return (
      <Flex direction="column" h="100vh" bgGradient={bgGradient} color="whiteAlpha.900">
        <Header title={HEADER_TITLE} />
        <Flex h="100vh" align="center" justify="center" bgGradient={bgGradient}>
        <Loader />
      </Flex>
      </Flex>
    );
  }

  if (error) {
    return (
      <Flex h="100vh" align="center" justify="center" bgGradient={bgGradient}>
        <Text color="red.400">{error}</Text>
      </Flex>
    );
  }

  if (!data) return null;

  const { audio_analysis: audio, technical_analysis: tech } = data;

  return (
    <Flex direction="column" h="100vh" bgGradient={bgGradient} color="whiteAlpha.900">
      <Header title={HEADER_TITLE} />
      <Flex flex="1" p={6} gap={4} overflow="hidden" minH={0}>
        <Box
          w="100%"
          flex="1"
          bg="#262934"
          p={5}
          borderRadius="2xl"
          shadow="xl"
          display="flex"
          flexDir="column"
          minH={0}
        >
          <Tabs
            variant="soft-rounded"
            colorScheme="purple"
            size="lg"
            flex="1"
            display="flex"
            flexDir="column"
          >
            <TabList bg={tabBg} p={1} borderTopRadius="lg">
              <Tab _selected={{ bg: "purple.600", color: "white" }} _hover={{ bg: "purple.500", color: "white" }} mr={1}>
                Audio Analysis
              </Tab>
              <Tab _selected={{ bg: "purple.600", color: "white" }} _hover={{ bg: "purple.500", color: "white" }}>
                Technical Analysis
              </Tab>
            </TabList>
            <TabPanels flex="1" bg={panelBg} p={2} borderBottomRadius="lg" overflowY="auto" maxH="78vh">
              {/* Audio Tab */}
              <TabPanel>
                <VStack align="start" spacing={6} mt={10}>
                  <AudioAnalysisScores
                    confidence={audio.confidence_score}
                    calmness={audio.calmness_score}
                    energy={audio.energy_score}
                    expressiveness={audio.expressiveness_score}
                  />

                  <Divider borderColor="gray.600" />
                  {reportType === "recruiter" ? (
                    <VStack align="center" spacing={2} w="100%">
                      <Text fontSize="lg" fontWeight="bold">
                        Summary
                      </Text>
                      <Text>{audio.recruiter_summary}</Text>
                    </VStack>
                  ) : (
                    <>
                      <VStack spacing={2} w="100%">
                        <Text align="center" fontSize="lg" fontWeight="bold">
                          Feedback
                        </Text>
                      </VStack>
                      <VStack align="start" w="100%">
                        <Text fontWeight="semibold">Positive:</Text>
                        <Text>{audio.candidate_feedback?.positive}</Text>
                        <Divider borderColor="gray.600" />
                        <Text fontWeight="semibold">Suggestions:</Text>
                        <Text>{audio.candidate_feedback?.suggestions}</Text>
                      </VStack>
                    </>
                  )}
                </VStack>
              </TabPanel>

              {/* Technical Tab */}
              <TabPanel>
                <VStack align="start" spacing={2} w="100%">
                  <Box w="100%" p={4} bg={tabBg} borderRadius="md">
                    {reportType === "recruiter" ? (
                      <VStack spacing={2} mt={2} w="100%">
                        <Text fontWeight="bold">Summary</Text>
                        <Text>{tech.recruiter_summary}</Text>
                      </VStack>
                    ) : (
                      <>
                        <VStack spacing={2} mt={2} w="100%">
                          <Text fontWeight="bold">Feedback</Text>
                        </VStack>
                        <Divider mb={5} mt={2} />
                        <VStack align="start" spacing={2} mt={2} w="100%">
                          <Text fontWeight="semibold">Positive:</Text>
                          <Text>{tech.candidate_feedback?.positive}</Text>
                          <Divider borderColor="gray.600" />
                          <Text fontWeight="semibold">Suggestions:</Text>
                          <Text>{tech.candidate_feedback?.suggestions}</Text>
                        </VStack>
                      </>
                    )}
                    <Divider borderColor="gray.600" my={2} />
                    <OverallTechnicalScore overallTechnicalScore={tech.overall_technical_score} />
                  </Box>
                  {tech.per_question.map((item, idx) => (
                    <GenerateReportTechnicalAccordian
                      key={idx}
                      questionNumber={idx + 1}
                      questionDetails={item}
                    />
                  ))}
                </VStack>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Box>
      </Flex>
    </Flex>
  );
};

export default GenerateReportPage;
