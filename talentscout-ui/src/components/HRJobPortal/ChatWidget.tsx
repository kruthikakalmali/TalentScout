// src/components/ChatWidget.tsx
import React from "react";
import { IconButton, Box, useDisclosure, Slide } from "@chakra-ui/react";
import { keyframes } from "@emotion/react";
import { ChatIcon, CloseIcon } from "@chakra-ui/icons";
import Chatbot from "./Chatbot";

const pulseRing = keyframes`
  0% {
    box-shadow: 0 0 0 0 rgba(128,90,213, 0.6);
  }
  70% {
    box-shadow: 0 0 0 20px rgba(128,90,213, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(128,90,213, 0);
  }
`;

const ChatWidget: React.FC = () => {
  const { isOpen, onToggle } = useDisclosure();

  return (
    <>
      <Box
        pos="fixed"
        bottom="6"
        right="6"
        width="72px"
        height="72px"
        display="flex"
        alignItems="center"
        justifyContent="center"
        zIndex="overlay"
        _before={{
          content: '""',
          pos: "absolute",
          top: 0,
          left: 0,
          width: "72px",
          height: "72px",
          borderRadius: "full",
          animation: `${pulseRing} 2s infinite`,
        }}
      >
        <IconButton
          aria-label={isOpen ? "Close chat" : "Open chat"}
          icon={isOpen ? <CloseIcon w={5} h={5} /> : <ChatIcon w={6} h={6} />}
          boxSize="60px"
          borderRadius="full"
          bgGradient="radial(circle at 30% 30%, purple.400, purple.700)"
          color="white"
          boxShadow="2xl"
          transition="all 0.3s"
          _hover={{
            transform: "scale(1.1)",
            bgGradient: "radial(circle at 30% 30%, purple.500, purple.800)",
          }}
          onClick={onToggle}
        />
      </Box>

      {isOpen && (
        <Slide direction="bottom" in={isOpen} style={{ zIndex: 999 }}>
          <Box
            position="fixed"
            bottom="50"
            right="50"
            width={["90%", "400px"]}
            height="560px"
            bg="whiteAlpha.200"
            borderRadius="2xl"
            boxShadow="xl"
            overflow="hidden"
          >
            <Chatbot />
          </Box>
        </Slide>
      )}
    </>
  );
};

export default ChatWidget;
