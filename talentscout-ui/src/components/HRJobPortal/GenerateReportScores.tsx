import React from "react";
import { VStack, HStack, Text, Box, useTheme, Flex, Divider } from "@chakra-ui/react";

interface TechAnalysisScoresProps {
  correctness: number;
  completeness: number;
  relevance: number;
  clarity: number;
  depth: number;
}

interface AudioAnalysisScoresProps {
  confidence: number;
  calmness: number;
  expressiveness: number;
  energy: number;
}

interface OverallTechnicalScoreProps {
  overallTechnicalScore: number;
}

const getGradientColor = (pct: number) => {
  if (pct < 25) return "red.500";
  if (pct < 50) return "orange.500";
  if (pct < 75) return "yellow.500";
  return "green.500";
};

export const TechAnalysisScores: React.FC<TechAnalysisScoresProps> = ({
  correctness,
  completeness,
  relevance,
  clarity,
  depth,
}) => {
  const theme = useTheme();

  const metrics = [
    {
      label: "Correctness",
      raw: correctness,
      pct: Math.round((correctness / 5) * 100),
    },
    {
      label: "Completeness",
      raw: completeness,
      pct: Math.round((completeness / 5) * 100),
    },
    {
      label: "Relevance",
      raw: relevance,
      pct: Math.round((relevance / 5) * 100),
    },
    {
      label: "Clarity",
      raw: clarity,
      pct: Math.round((clarity / 5) * 100),
    },
    {
      label: "Depth",
      raw: depth,
      pct: Math.round((depth / 5) * 100),
    },
  ];

  return (
    <Flex justifyContent={"space-evenly"} align="start">
      {metrics.map(({ label, raw, pct }) => (
        <VStack key={label} spacing={1} align="start">
          <Text fontSize="sm" fontWeight="medium">
            {label}
          </Text>

          <Box
            w="200px"
            h="10px"
            bg={theme.colors.gray[200]}
            borderRadius="md"
            overflow="hidden"
          >
            <Box
              h="100%"
              w={`${pct}%`}
              bg={getGradientColor(pct)}
              transition="width 0.3s ease"
            />
          </Box>

          <Text fontSize="xs" color="gray.600">
            {raw}/5 ({pct}%)
          </Text>
        </VStack>
      ))}
    </Flex>
  );
};

export const AudioAnalysisScores: React.FC<AudioAnalysisScoresProps> = ({
  confidence,
  calmness,
  expressiveness,
  energy,
}) => {
  const theme = useTheme();

  const metrics = [
    {
      label: "Confidence",
      raw: confidence,
      pct: Math.round((confidence / 5) * 100),
    },
    {
      label: "Calmness",
      raw: calmness,
      pct: Math.round((calmness / 5) * 100),
    },
    {
      label: "Expressiveness",
      raw: expressiveness,
      pct: Math.round((expressiveness / 5) * 100),
    },
    {
      label: "Energy",
      raw: energy,
      pct: Math.round((energy / 5) * 100),
    },
  ];

  return (
    <Flex justifyContent={"space-evenly"} align="start" w={"100%"}>
      {metrics.map(({ label, raw, pct }) => (
        <VStack key={label} spacing={1} align="start">
          <Text fontSize="sm" fontWeight="medium">
            {label}
          </Text>

          <Box
            w="200px"
            h="10px"
            bg={theme.colors.gray[200]}
            borderRadius="md"
            overflow="hidden"
          >
            <Box
              h="100%"
              w={`${pct}%`}
              bg={getGradientColor(pct)}
              transition="width 0.3s ease"
            />
          </Box>

          <Text fontSize="xs" color="gray.600">
            {raw}/5 ({pct}%)
          </Text>
        </VStack>
      ))}
    </Flex>
  );
};

export const OverallTechnicalScore: React.FC<OverallTechnicalScoreProps> = ({
  overallTechnicalScore,
}) => {
  const theme = useTheme();
  const pct = Math.round((overallTechnicalScore / 5) * 100);

  return (
    <VStack align="center" spacing={1} w="100%">
      <Text fontSize="sm" fontWeight="medium">
        Overall Technical Score
      </Text>
      <Box
        w="200px"
        h="10px"
        bg={theme.colors.gray[200]}
        borderRadius="md"
        overflow="hidden"
      >
        <Box
          h="100%"
          w={`${pct}%`}
          bg={"green.500"}
          transition="width 0.3s ease"
        />
      </Box>

      <Text fontSize="xs" color="gray.600">
        {pct}%
      </Text>
    </VStack>
  );
};
