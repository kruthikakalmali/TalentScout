import React from "react";
import {
  Box,
  Text,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
} from "@chakra-ui/react";

interface QuestionHistoryObject {
  question: string;
  answer: string;
}

interface QuestionHistoryProps {
  questionsList: QuestionHistoryObject[];
}

const QuestionHistory: React.FC<QuestionHistoryProps> = ({ questionsList }) => (
  <Box
    w="30%"
    bg="whiteAlpha.100"
    backdropFilter="blur(8px)"
    borderRadius="md"
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
      color="whiteAlpha.900"
      mb={5}
      flexShrink={0}
    >
      Questions History
    </Text>
    <Box id="questions-history-body" flex="1" overflowY="auto" maxH={"77vh"}>
      <Accordion allowMultiple>
        {questionsList.map(({ question, answer }, idx) => (
          <AccordionItem
            key={idx}
            border="none"
            mb={2}
            borderRadius="md"
            overflow="hidden"
          >
            <AccordionButton
              bg="whiteAlpha.50"
              _hover={{ bg: "whiteAlpha.200" }}
              _expanded={{ bg: "whiteAlpha.300" }}
              px={3}
              py={3}
            >
              <Box flex="1" textAlign="left">
                <Text fontWeight="medium" color="whiteAlpha.900">
                  {`Q${idx + 1}: ${question}`}
                </Text>
                <Text fontSize="sm" color="whiteAlpha.700" noOfLines={1}>
                  {answer}
                </Text>
              </Box>
              <AccordionIcon color="whiteAlpha.700" />
            </AccordionButton>
            <AccordionPanel
              px={4}
              pb={4}
              maxH="300px"
              overflowY="auto"
              bg="whiteAlpha.200"
            >
              <Text color="whiteAlpha.900" whiteSpace="pre-wrap">
                {answer}
              </Text>
            </AccordionPanel>
          </AccordionItem>
        ))}
      </Accordion>
    </Box>
  </Box>
);

export default React.memo(QuestionHistory);
