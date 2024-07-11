const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const videoDirectory = 'C:/Users/smile/OneDrive/Documents/higherlayer/videos';

app.use(cors()); // Enable CORS for all routes

// Endpoint to list videos
app.get('/videos', (req, res) => {
    fs.readdir(videoDirectory, (err, files) => {
        if (err) {
            console.error('Error reading video directory:', err);
            return res.status(500).send('Error reading video directory');
        }

        const videoFiles = files.filter(file => path.extname(file).toLowerCase() === '.mp4');
        res.json(videoFiles);
    });
});

// Static file serving for videos
app.use('/video', express.static(videoDirectory));

const PORT = 3000; // Use your controller server port
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
