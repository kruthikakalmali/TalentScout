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
} from "@chakra-ui/react";
import { SimilarityScore, OtherScores } from "./ApplicantScores";

interface ApplicantData {
  applicant_id: string;
  name: string;
  email: string;
  similarity_score: number;
  skill_match: number;
  experience_relevance: number;
  cultural_fit_guess: number;
  strengths: string;
  potential_gaps: string;
  overall_fit_summary: string;
}

interface ApplicantAccordionProps {
  applicant: ApplicantData;
  onInvite: (email: string) => void;
}

const ApplicantAccordion: React.FC<ApplicantAccordionProps> = ({
  applicant,
  onInvite,
}) => {
  const bgMain = useColorModeValue("#1a202c", "#1a202c");
  const containerBg = useColorModeValue("#2d3748", "#2d3748");
  const panelBg = useColorModeValue("#2c313c", "#2c313c");

  return (
    <Accordion allowToggle>
      <AccordionItem border="none" bg={bgMain} mb={4}>
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
              bg={isExpanded ? panelBg : containerBg}
              borderLeft="4px solid"
              borderLeftColor="purple.500"
              borderRight="4px solid"
              borderRightColor="purple.500"
            >
              <Flex w="100%" align="center" justify="space-between">
                {/* Left block */}
                <VStack align="start" spacing={1}>
                  <Text fontWeight="bold" fontSize="xl">
                    {applicant.name}
                  </Text>
                  <Text fontSize="sm" color="gray.300">
                    Email ID: {applicant.email}
                  </Text>
                  <Text fontSize="sm" color="gray.300">
                    Applicant ID: {applicant.applicant_id}
                  </Text>
                </VStack>

                {/* Right block */}
                <HStack spacing={4} align="center">
                  <SimilarityScore
                    similarityScore={applicant.similarity_score}
                  />
                  <AccordionIcon color="gray.300" />
                </HStack>
              </Flex>
            </AccordionButton>

            <AccordionPanel
              bg={panelBg}
              borderRadius="md"
              mt={-1}
              px={4}
              py={5}
              borderLeft="4px solid"
              borderLeftColor="purple.500"
              borderRight="4px solid"
              borderRightColor="purple.500"
            >
              <OtherScores
                skillMatch={applicant.skill_match}
                experienceRelevance={applicant.experience_relevance}
                culturalFitGuess={applicant.cultural_fit_guess}
              />

              <VStack align="start" spacing={4} mb={6}>
                <Box>
                  <Text fontWeight="semibold" mb={1} color="white">
                    Strengths
                  </Text>
                  <Text fontSize="sm" color="gray.300">
                    {applicant.strengths}
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" mb={1} color="white">
                    Potential Gaps
                  </Text>
                  <Text fontSize="sm" color="gray.300">
                    {applicant.potential_gaps}
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" mb={1} color="white">
                    Overall Fit
                  </Text>
                  <Text fontSize="sm" color="gray.300">
                    {applicant.overall_fit_summary}
                  </Text>
                </Box>
              </VStack>

              <Box textAlign="right">
                <Button
                  colorScheme="purple"
                  onClick={() => onInvite(applicant.email)}
                >
                  Send Interview Invite
                </Button>
              </Box>
            </AccordionPanel>
          </>
        )}
      </AccordionItem>
    </Accordion>
  );
};

export default ApplicantAccordion;
