import React from "react";
import { VStack, HStack, Text, Box, useTheme, Flex } from "@chakra-ui/react";

interface SimilarityScoreProps {
  similarityScore: number;
}

interface OtherScoresProps {
  skillMatch: number;
  experienceRelevance: number;
  culturalFitGuess: number;
}

const getGradientColor = (pct: number) => {
  if (pct < 25) return "red.500";
  if (pct < 50) return "orange.500";
  if (pct < 75) return "yellow.500";
  return "green.500";
};

export const SimilarityScore: React.FC<SimilarityScoreProps> = ({
  similarityScore,
}) => {
  const theme = useTheme();
  const pct = Math.round(similarityScore * 100);

  return (
    <VStack align="start" spacing={1} w="100%">
      <Text fontSize="sm" fontWeight="medium">
        Similarity Score
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
        {pct}%
      </Text>
    </VStack>
  );
};

export const OtherScores: React.FC<OtherScoresProps> = ({
  skillMatch,
  experienceRelevance,
  culturalFitGuess,
}) => {
  const theme = useTheme();

  const metrics = [
    {
      label: "Skill Match",
      raw: skillMatch,
      pct: Math.round((skillMatch / 10) * 100),
    },
    {
      label: "Experience Relevance",
      raw: experienceRelevance,
      pct: Math.round((experienceRelevance / 10) * 100),
    },
    {
      label: "Cultural Fit Guess",
      raw: culturalFitGuess,
      pct: Math.round((culturalFitGuess / 10) * 100),
    },
  ];

  return (
    <Flex justifyContent={'space-evenly'} align="start">
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
            {raw}/10 ({pct}%)
          </Text>
        </VStack>
      ))}
    </Flex>
  );
};
