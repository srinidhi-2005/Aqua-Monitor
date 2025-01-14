import numpy as np

# Function to initialize weights with small random values
def initialize_weights(shape):
    return np.random.randn(*shape) * 0.1

# ReLU activation function
def relu(x):
    return np.maximum(0, x)

# Derivative of ReLU activation function
def relu_derivative(x):
    return (x > 0).astype(float)

# Sigmoid activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivative of sigmoid activation function
def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

# Convolutional Layer
class ConvLayer:
    def __init__(self, num_filters, filter_size):
        self.num_filters = num_filters
        self.filter_size = filter_size
        # Initialize filters with random values
        self.filters = initialize_weights((num_filters, filter_size, filter_size, 3))

    def forward(self, input):
        self.last_input = input
        h, w = input.shape[:2]
        output_height = h - self.filter_size + 1
        output_width = w - self.filter_size + 1
        # Create an empty output array
        output = np.zeros((output_height, output_width, self.num_filters))
        for i in range(output_height):
            for j in range(output_width):
                # Get the region of the input
                region = input[i:i+self.filter_size, j:j+self.filter_size]
                for f in range(self.num_filters):
                    # Apply the filter to the region
                    output[i, j, f] = np.sum(region * self.filters[f])
        return output

    def backward(self, dL_dout, learning_rate):
        # Create an empty array for filter gradients
        dL_dfilters = np.zeros(self.filters.shape)
        for i in range(self.last_input.shape[0] - self.filter_size + 1):
            for j in range(self.last_input.shape[1] - self.filter_size + 1):
                # Get the region of the input
                region = self.last_input[i:i+self.filter_size, j:j+self.filter_size]
                for f in range(self.num_filters):
                    # Calculate the gradient for the filter
                    dL_dfilters[f] += dL_dout[i, j, f] * region
        # Update the filters
        self.filters -= learning_rate * dL_dfilters

# Max Pooling Layer
class MaxPool:
    def __init__(self, pool_size):
        self.pool_size = pool_size

    def forward(self, input):
        self.last_input = input
        h, w, num_filters = input.shape
        output_height = h // self.pool_size
        output_width = w // self.pool_size
        # Create an empty output array
        output = np.zeros((output_height, output_width, num_filters))
        for i in range(output_height):
            for j in range(output_width):
                # Get the region of the input
                region = input[i*self.pool_size:(i+1)*self.pool_size, j*self.pool_size:(j+1)*self.pool_size]
                # Apply max pooling
                output[i, j] = np.max(region, axis=(0, 1))
        return output

    def backward(self, dL_dout):
        # Create an empty array for input gradients
        dL_dinput = np.zeros(self.last_input.shape)
        for i in range(dL_dout.shape[0]):
            for j in range(dL_dout.shape[1]):
                # Get the region of the input
                region = self.last_input[i*self.pool_size:(i+1)*self.pool_size, j*self.pool_size:(j+1)*self.pool_size]
                h, w, f = region.shape
                max_val = np.max(region, axis=(0, 1))
                for x in range(h):
                    for y in range(w):
                        for z in range(f):
                            # Distribute the gradient to the max value
                            if region[x, y, z] == max_val[z]:
                                dL_dinput[i*self.pool_size+x, j*self.pool_size+y, z] += dL_dout[i, j, z]
        return dL_dinput

# Dense (Fully Connected) Layer
class Dense:
    def __init__(self, input_size, output_size):
        # Initialize weights and biases
        self.weights = initialize_weights((input_size, output_size))
        self.biases = np.zeros(output_size)

    def forward(self, input):
        self.last_input = input.reshape(1, -1)  # Flatten the input
        # Calculate the output
        return np.dot(self.last_input, self.weights) + self.biases

    def backward(self, dL_dout, learning_rate):
        dL_dout = dL_dout.reshape(1, -1)
        
        # Calculate gradients
        dL_dweights = np.dot(self.last_input.T, dL_dout)
        dL_dbiases = dL_dout.sum(axis=0)
        dL_dinput = np.dot(dL_dout, self.weights.T)
        
        # Update weights and biases
        self.weights -= learning_rate * dL_dweights
        self.biases -= learning_rate * dL_dbiases
        
        # Return gradient for previous layer
        return dL_dinput