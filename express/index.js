const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

app.use(express.json());

const sendRequest = async (endpoint, data, res) => {
  try {
    const response = await axios.post(`http://localhost:5000${endpoint}`, data); // Use localhost for internal communication
    res.send(response.data);
  } catch (error) {
    res.status(500).send({ status: 'error', message: error.message });
  }
};

const getRequest = async (endpoint, res) => {
  try {
    const response = await axios.get(`http://localhost:5000${endpoint}`); // Use localhost for internal communication
    res.send(response.data);
  } catch (error) {
    res.status(500).send({ status: 'error', message: error.message });
  }
}

app.get('/', (req, res) => {
  getRequest('/', res);
});


app.post('/start', (req, res) => {
  const config = req.body.config;
  sendRequest('/play', { config }, res);
});

app.post('/update-volume', (req, res) => {
  const { trackId, volume } = req.body;
  sendRequest('/update-volume', { trackId, volume }, res);
});

app.post('/stop', (req, res) => {
  const { trackId } = req.body;
  sendRequest('/stop', { trackId }, res);
});

app.post('/pause', (req, res) => {
  const { trackId } = req.body;
  sendRequest('/pause', { trackId }, res);
});

app.post('/stop-all', (req, res) => {
  sendRequest('/stop-all', {}, res);
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
