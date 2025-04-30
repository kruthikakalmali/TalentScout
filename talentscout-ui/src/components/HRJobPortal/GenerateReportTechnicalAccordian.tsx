import React from "react";
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Box,
  Text,
  HStack,
  VStack,
  Button,
  useColorModeValue,
  Flex,
  Spacer,
  Divider,
} from "@chakra-ui/react";
import {
  TechAnalysisScores,
  OverallTechnicalScore,
} from "./GenerateReportScores";

interface Scores {
  correctness: number;
  completeness: number;
  relevance: number;
  clarity: number;
  depth: number;
}

interface QuestionDetails {
  question: string;
  answer_excerpt: string;
  scores: Scores;
  summary: string;
}

interface GenerateReportTechnicalAccordianProps {
  questionNumber: number;
  questionDetails: QuestionDetails;
}

const GenerateReportTechnicalAccordian: React.FC<
  GenerateReportTechnicalAccordianProps
> = ({ questionNumber, questionDetails }) => {
  const bgMain = useColorModeValue("#1a202c", "#1a202c");
  const containerBg = useColorModeValue("#2d3748", "#2d3748");
  const panelBg = useColorModeValue("#2c313c", "#2c313c");

  return (
    <Accordion allowToggle>
      <AccordionItem border="none" bg={bgMain} mb={2}>
        {({ isExpanded }) => (
          <>
            <AccordionButton
              borderTopRadius="md"
              borderBottomRadius="md"
              _expanded={{ borderBottomRadius: 0 }}
              boxShadow="md"
              px={4}
              py={3}
              _hover={{ bg: panelBg }}
              bg={containerBg}
              borderLeft="4px solid"
              borderLeftColor="purple.500"
              borderRight="4px solid"
              borderRightColor="purple.500"
            >
              <Flex w="100%" align="center" justify="space-between">
                <VStack align="start" spacing={1}>
                  <Text fontWeight="bold" fontSize="lg">
                    Q{questionNumber}: {questionDetails.question}
                  </Text>
                </VStack>
                <AccordionIcon color="gray.300" />
              </Flex>
            </AccordionButton>

            <AccordionPanel
              bg={containerBg}
              _hover={{ bg: panelBg }}
              borderRadius="md"
              mt={-1}
              px={4}
              py={5}
              borderLeft="4px solid"
              borderLeftColor="purple.500"
              borderRight="4px solid"
              borderRightColor="purple.500"
            >
              <VStack align="center" spacing={2} w="100%" mb={5}>
                <Text fontSize="lg" fontWeight="bold">
                  Answer Excerpt
                </Text>
                <Divider mb={5} />
                <Text>{questionDetails.answer_excerpt}</Text>
              </VStack>
              <Divider borderColor="gray.600" my={5} />
              <VStack align="center" spacing={2} w="100%" mb={2}>
                <Text fontSize="lg" fontWeight="bold">
                  Technical Scores
                </Text>
              </VStack>

              <Divider mb={5} />
              <TechAnalysisScores
                correctness={questionDetails.scores.correctness}
                completeness={questionDetails.scores.completeness}
                relevance={questionDetails.scores.relevance}
                clarity={questionDetails.scores.clarity}
                depth={questionDetails.scores.depth}
              />
              <Divider borderColor="gray.600" mt={5} mb={2} />
              <VStack align="center" spacing={2} w="100%">
                <Text fontSize="lg" fontWeight="bold">
                  Summary
                </Text>
                <Divider mb={5} />
                <Text>{questionDetails.summary}</Text>
              </VStack>
            </AccordionPanel>
          </>
        )}
      </AccordionItem>
    </Accordion>
  );
};

export default GenerateReportTechnicalAccordian;
