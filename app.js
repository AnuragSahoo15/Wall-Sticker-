// Import TensorFlow.js library
import * as tf from '@tensorflow/tfjs';

// Function to load the model
async function loadModel() {
    const model = await tf.loadLayersModel('tfjs_model/model.json');
    console.log('Model loaded successfully!');
    return model;
}

// Call the function to load the model
loadModel().then(model => {
    // Use the model for inference or other tasks
}).catch(err => {
    console.error('Error loading the model:', err);
});
