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
  useDisclosure,
  Input,
  Textarea,
  FormControl,
  FormLabel,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  useToast,
  Center
} from "@chakra-ui/react";
import axios from "axios";
import Header from "../Header/Header";
import Loader from "../Loader";
import { PROD_HOST_URL } from "../../constants";

interface Job {
  id: string;
  job_id: string;
  job_role: string;
  description: string;
}

interface Applicant {
  name: string;
  email: string;
  extracted_info: string;
}

const HRJobPortal: React.FC = () => {
  const bgGradient = useColorModeValue(
    "linear(to-br, gray.900, gray.800)",
    "linear(to-br, gray.900, gray.800)"
  );
  const containerBg = useColorModeValue("gray.700", "gray.600");
  const outlineButtonColor = '#1e3660'
  const modalBg ="#262934";
  const modalColor = "whiteAlpha.900";

  const {
    isOpen: isCreateOpen,
    onOpen: onCreateOpen,
    onClose: onCreateClose,
  } = useDisclosure();
  const {
    isOpen: isDescOpen,
    onOpen: onDescOpen,
    onClose: onDescClose,
  } = useDisclosure();
  const {
    isOpen: isApplicantsOpen,
    onOpen: onApplicantsOpen,
    onClose: onApplicantsClose,
  } = useDisclosure();
  const {
    isOpen: isCandidateProfileOpen,
    onOpen: onCandidateProfileOpen,
    onClose: onCandidateProfileClose,
  } = useDisclosure();

  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [selectedApplicant, setSelectedApplicant] = useState<Applicant | null>(null);
  const [newJobRole, setNewJobRole] = useState("");
  const [newJobId, setNewJobId] = useState("");
  const [newJobDesc, setNewJobDesc] = useState("");
  const [creating, setCreating] = useState(false);
  const [applicants, setApplicants] = useState<Applicant[]>([]);
  const [applicantsLoading, setApplicantsLoading] = useState(false);
  const toast = useToast();

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${PROD_HOST_URL}/get_all_jobs`);
      setJobs(response.data.jobs || []);
    } catch (error) {
      console.error(error);
      toast({ title: "Error fetching jobs", status: "error", duration: 3000 });
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDesc = (job: Job) => {
    setSelectedJob(job);
    onDescOpen();
  };

  const handleOpenProfile = (applicant: Applicant) => {
    setSelectedApplicant(applicant);
    onCandidateProfileOpen();
  };

  const handleOpenApplicants = (job: Job) => {
    setSelectedJob(job);
    onApplicantsOpen();
    fetchApplicants(job.job_id);
  };

  const fetchApplicants = async (jobId: string) => {
    setApplicantsLoading(true);
    try {
      const response = await axios.get(
        `${PROD_HOST_URL}/get_applications_by_job_id?job_id=${jobId}`
      );
      setApplicants(response.data.applications || []);
    } catch (error) {
      console.error(error);
      toast({
        title: "Error fetching applicants",
        status: "error",
        duration: 3000,
      });
    } finally {
      setApplicantsLoading(false);
    }
  };

  const handleSendInvite = async (applicant: Applicant) => {
    console.log("Invitation Sent!", applicant)
    // try {
    //   await axios.post(`${PROD_HOST_URL}/send_invite`, {
    //     job_id: selectedJob?.job_id,
    //     email: applicant.email,
    //   });
    //   toast({
    //     title: `Invite sent to ${applicant.name}`,
    //     status: "success",
    //     duration: 3000,
    //   });
    // } catch (error) {
    //   console.error(error);
    //   toast({ title: "Error sending invite", status: "error", duration: 3000 });
    // }
  };

  const handleCreateJob = async () => {
    if (!newJobRole || !newJobDesc) {
      toast({
        title: "Please enter a role and description",
        status: "warning",
        duration: 3000,
      });
      return;
    }
    setCreating(true);
    try {
      const formData = new FormData();
      formData.append("job_role", newJobRole);
      formData.append("job_id", newJobId);
      formData.append("description", newJobDesc);
      await axios.post(`${PROD_HOST_URL}/create_job`, formData);
      toast({ title: "Job created", status: "success", duration: 3000 });
      onCreateClose();
      setNewJobRole("");
      setNewJobId("");
      setNewJobDesc("");
      fetchJobs();
    } catch (error) {
      console.error(error);
      toast({ title: "Error creating job", status: "error", duration: 3000 });
    } finally {
      setCreating(false);
    }
  };

  return (
    <Flex
      direction="column"
      h="100vh"
      bgGradient={bgGradient}
      color="whiteAlpha.900"
    >
      <Header title="HR Dashboard" />

      {loading ? (
        <Flex justify="center" align="center" h="100%">
          <Loader />
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
            <Flex justify="flex-end" mb={6}>
              <Button size="lg" colorScheme="purple" onClick={onCreateOpen}>
                + New Job
              </Button>
            </Flex>
            <VStack align="stretch" spacing={4} overflow="auto" height="70vh">
              {jobs.map((job) => (
                <Box key={job.id} p={6} bg={containerBg} borderRadius="2xl">
                  <HStack spacing={4}>
                    <VStack align="start" spacing={1}>
                      <Text fontWeight="bold" fontSize="xl">
                        {job.job_role}
                      </Text>
                      <Text fontSize="sm" color="gray.300">
                        Job ID: {job.job_id}
                      </Text>
                    </VStack>
                    <Spacer />
                    <HStack spacing={3}>
                      <Button
                        size="md"
                        colorScheme="purple"
                        variant="outline"
                        onClick={() => handleOpenDesc(job)}
                      >
                        View Job Description
                      </Button>
                      <Button
                        size="md"
                        colorScheme="purple"
                        onClick={() => handleOpenApplicants(job)}
                      >
                        View Top Applicants
                      </Button>
                    </HStack>
                  </HStack>
                </Box>
              ))}
            </VStack>
          </Box>
        </Flex>
      )}

      {/* Create Job Modal */}
      <Modal
        isOpen={isCreateOpen}
        onClose={onCreateClose}
        size="2xl"
        isCentered
      >
        <ModalOverlay />
        <ModalContent bg={modalBg} color={modalColor} maxH="70vh">
          <ModalHeader textAlign="center">Create New Job</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <FormControl mb={4}>
              <FormLabel>Job Role</FormLabel>
              <Input
                placeholder="Enter Job Role"
                value={newJobRole}
                onChange={(e) => setNewJobRole(e.target.value)}
              />
            </FormControl>
            <FormControl mb={4}>
              <FormLabel>Job ID (optional)</FormLabel>
              <Input
                placeholder="Enter Job ID"
                value={newJobId}
                onChange={(e) => setNewJobId(e.target.value)}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Job Description</FormLabel>
              <Textarea
                placeholder="Enter Job Description"
                minH="150px"
                maxH="300px"
                value={newJobDesc}
                onChange={(e) => setNewJobDesc(e.target.value)}
                rows={6}
              />
            </FormControl>
          </ModalBody>
          <ModalFooter>
            <Button
              colorScheme="purple"
              mr={3}
              onClick={handleCreateJob}
              isLoading={creating}
            >
              Create
            </Button>
            <Button
              variant="outline"
              colorScheme="purple"
              onClick={onCreateClose}
            >
              Cancel
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      {/* Job Description Modal */}
      <Modal isOpen={isDescOpen} onClose={onDescClose} size="xl" isCentered>
        <ModalOverlay />
        <ModalContent bg={modalBg} color={modalColor} maxH="80vh">
          <ModalHeader textAlign="center">Job Description</ModalHeader>
          <ModalCloseButton />
          <ModalBody
            overflowY="auto"
            maxH="calc(80vh - 120px)"
            whiteSpace="pre-wrap"
            bg={containerBg}
            pl={3}
            pr={3}
            mr={4}
            ml={4}
            borderRadius="lg"
          >
            {selectedJob?.description || "No description available."}
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="purple" onClick={onDescClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      {/* Applicants Modal */}
      <Modal
        isOpen={isApplicantsOpen}
        onClose={onApplicantsClose}
        size="5xl"
        isCentered
      >
        <ModalOverlay />
        <ModalContent bg={modalBg} color={modalColor} minH="80vh" maxH="80vh">
          <ModalHeader textAlign="center">Top Applicants</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            {applicantsLoading ? (
                <Center h="65vh"><Loader /></Center>
            ) : applicants.length > 0 ? (
              <VStack align="stretch" spacing={4} overflow="auto" height="65vh">
                {applicants.map((applicant, index) => (
                  <Box key={index} p={6} bg={containerBg} borderRadius="2xl">
                    <HStack spacing={4}>
                      <VStack align="start" spacing={1}>
                        <Text fontWeight="bold" fontSize="xl">
                          {applicant.name}
                        </Text>
                        <Text fontSize="sm" color="gray.300">
                          Email ID: {applicant.email}
                        </Text>
                      </VStack>
                      <Spacer />
                      <HStack spacing={3}>
                        <Button
                          size="md"
                          colorScheme="purple"
                          variant="outline"
                          onClick={() => handleOpenProfile(applicant)}
                        >
                          View Profile
                        </Button>
                        <Button
                          size="md"
                          colorScheme="purple"
                          onClick={() => handleSendInvite(applicant)}
                        >
                          Send Interview Invite
                        </Button>
                      </HStack>
                    </HStack>
                  </Box>
                ))}
              </VStack>
            ) : (
              <Text color="gray.400"><Center h="65vh">No applicants found.</Center></Text>
            )}
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="purple" onClick={onApplicantsClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      {/* Candidate Profile Modal */}
      <Modal
        isOpen={isCandidateProfileOpen}
        onClose={onCandidateProfileClose}
        size="xl"
        isCentered
      >
        <ModalOverlay />
        <ModalContent bg={modalBg} color={modalColor} maxH="80vh">
          <ModalHeader textAlign="center">Candidate's Profile</ModalHeader>
          <ModalCloseButton />
          <ModalBody
            overflowY="auto"
            flex={1}
            maxH="calc(80vh - 120px)"
            whiteSpace="pre-wrap"
            bg={containerBg}
            pl={3}
            pr={3}
            mr={4}
            ml={4}
            borderRadius="lg"
          >
            {`${selectedApplicant?.extracted_info}` || "No Profile available."}
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="purple" onClick={onCandidateProfileClose}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Flex>
  );
};

export default HRJobPortal;
