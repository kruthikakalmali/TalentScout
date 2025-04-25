const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const port = 3001;

app.use(bodyParser.json());

// Endpoint to get embeddings and compare them
app.post('/match', async (req, res) => {
  try {
    const { jd, candidates } = req.body;

    // Get JD embedding from Azure
    const jdEmbedding = await getEmbedding(jd);
    if (!jdEmbedding) {
      return res.status(400).send('Failed to get JD embedding');
    }

    // Get candidate embeddings and compare
    const results = [];
    for (let candidate of candidates) {
      const candidateEmbedding = await getEmbedding(candidate.skills.join(' '));
      if (!candidateEmbedding) {
        continue;
      }

      const similarity = cosineSimilarity(jdEmbedding, candidateEmbedding);
      results.push({ ...candidate, similarity });
    }

    results.sort((a, b) => b.similarity - a.similarity);

    res.json(results);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).send('Server error');
  }
});

// Helper function to get embeddings from Azure
const getEmbedding = async (text) => {
  try {
    const response = await axios.post(
      process.env.AZURE_ENDPOINT,
      { input: text },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${process.env.AZURE_API_KEY}`,
        },
      }
    );
    return response.data.data[0].embedding;
  } catch (error) {
    console.error('Error fetching embedding:', error);
    return null;
  }
};

// Helper function to calculate cosine similarity between two vectors
const cosineSimilarity = (vec1, vec2) => {
  let dotProduct = 0;
  let magnitude1 = 0;
  let magnitude2 = 0;

  for (let i = 0; i < vec1.length; i++) {
    dotProduct += vec1[i] * vec2[i];
    magnitude1 += vec1[i] ** 2;
    magnitude2 += vec2[i] ** 2;
  }

  const magnitude = Math.sqrt(magnitude1) * Math.sqrt(magnitude2);
  return dotProduct / magnitude;
};

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
