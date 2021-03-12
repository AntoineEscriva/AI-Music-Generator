# !/usr/bin/python3
#coding: utf-8

import torch
from torch import nn
import numpy as np
import time


def one_hot_encode(sequence, dict_size, seq_len, batch_size):
    # Creating a multi-dimensional array of zeros with the desired output shape
    features = np.zeros((batch_size, seq_len, dict_size), dtype=np.float32)
    
    # Replacing the 0 at the relevant character index with a 1 to represent that character
    for i in range(batch_size):
        for u in range(seq_len):
            features[i, u, sequence[i][u]] = 1
    return features


#return nb_samples samples from input_t & target_t
def sample_seq(nb_samples, total, input_t, target_t):
    global new_input, new_target, indexes
    indexes = np.random.randint(0, total-1, nb_samples)
    input_shape = input_seq.size()
    target_shape = target_seq.size()
    new_input = torch.randn((nb_samples, input_shape[1], input_shape[2]), dtype=torch.float32)
    new_target = torch.randn((nb_samples, target_shape[1]), dtype=torch.float32)

    for a in range(len(indexes)):
        new_input[a] = input_seq[indexes[a]].detach().clone()
        new_target[a] = target_seq[indexes[a]].detach().clone()
    return new_input, new_target



class Model(nn.Module):
    def __init__(self, input_size, output_size, hidden_dim, n_layers):
        super(Model, self).__init__()

        # Defining some parameters
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        #Defining the layers
        # RNN Layer
        self.rnn = nn.RNN(input_size, hidden_dim, n_layers, batch_first=True)   #essayer GRU (ou LSTM)
        # Fully connected layer
        self.fc = nn.Linear(hidden_dim, output_size)
    
    def forward(self, x):
        
        batch_size = x.size(0)

        # Initializing hidden state for first input using method defined below
        hidden = self.init_hidden(batch_size)

        # Passing in the input and hidden state into the model and obtaining outputs
        out, hidden = self.rnn(x, hidden)
        
        # Reshaping the outputs such that it can be fit into the fully connected layer
        out = out.contiguous().view(-1, self.hidden_dim)
        out = self.fc(out)
        
        return out, hidden
    
    def init_hidden(self, batch_size):
        # This method generates the first hidden state of zeros which we'll use in the forward pass
        # We'll send the tensor holding the hidden state to the device we specified earlier as well
        hidden = torch.zeros(self.n_layers, batch_size, self.hidden_dim).to(device)
        return hidden


# This function takes in the model and character as arguments and returns the next character prediction and hidden state
def predict(model, character):
    # One-hot encoding our input to fit into the model
    character = np.array([[char2int[c] for c in character]])
    character = one_hot_encode(character, dict_size, character.shape[1], 1)
    character = torch.from_numpy(character)
    character = character.to(device)
    
    out, hidden = model(character)

    prob = nn.functional.softmax(out[-1], dim=0).data
    # Taking the class with the highest probability score from the output
    char_ind = torch.max(prob, dim=0)[1].item()

    return int2char[char_ind], hidden


# This function takes the desired output length and input characters as arguments, returning the produced sentence
def sample(model, out_len, start):
    model.eval() # eval mode
    ## start = start.lower() # WHY ?
    # First off, run through the starting characters
    chars = [ch for ch in start]
    size = out_len - len(chars)
    # Now pass in the previous characters and get a new one
    for ii in range(size):
        char, h = predict(model, chars)
        chars.append(char)

    return ''.join(chars)



def rnn(txt):
	#########################
	# Debut premier section
	#########################


	# torch.cuda.is_available() checks and returns a Boolean True if a GPU is available, else it'll return False
	is_cuda = torch.cuda.is_available()

	# If we have a GPU available, we'll set our device to GPU. We'll use this device variable later in our code.
	global device, int2char, char2int, dict_size
	if is_cuda:
		device = torch.device("cuda")
		print("GPU is available")
	else:
		device = torch.device("cpu")
		print("GPU not available, CPU used")


	taille = 10 #length of a sequence # de 100 à 200 généralement (50 pk pas)
	batch_len = 16 # 16 ou 32
	id_last_car = len(txt)-taille #index of the last character to parse for creating the sequences
	text = []


	for i in range(id_last_car):
		text.append(txt[i:i+taille+1])


	# Join all the sentences together and extract the unique characters from the combined sentences
	chars = set(''.join(text))

	# Creating a dictionary that maps integers to the characters
	int2char = dict(enumerate(chars))

	# Creating another dictionary that maps characters to integers
	char2int = {char: ind for ind, char in int2char.items()}


	# Finding the length of the longest string in our data
	maxlen = len(max(text, key=len))



	# Creating lists that will hold our input and target sequences
	input_seq = []
	target_seq = []

	for i in range(len(text)):
		# Remove last character for input sequence
	  input_seq.append(text[i][:-1])
		
		# Remove first character for target sequence
	  target_seq.append(text[i][1:])
	  #print("Input Sequence: {}\nTarget Sequence: {}".format(input_seq[i], target_seq[i]))


	for i in range(len(text)):
		input_seq[i] = [char2int[character] for character in input_seq[i]]
		target_seq[i] = [char2int[character] for character in target_seq[i]]


	dict_size = len(char2int)
	seq_len = maxlen - 1
	batch_size = len(text)

	##################
	#Fin premiere section
	##################



	###################################
	# Debut 2e section
	###################################
	# Input shape --> (Batch Size, Sequence Length, One-Hot Encoding Size)
	input_seq = one_hot_encode(input_seq, dict_size, seq_len, batch_size)

	input_seq = torch.from_numpy(input_seq)
	target_seq = torch.Tensor(target_seq)
	###################################
	# Fin 2e section
	###################################







	# Instantiate the model with hyperparameters
	model = Model(input_size=dict_size, output_size=dict_size, hidden_dim=512, n_layers=1)
	# We'll also set the model to the device that we defined earlier
	model = model.to(device)

	# set the input_seq ant target_seq to the device used
	input_seq = input_seq.to(device) 
	target_seq = target_seq.to(device)


	# Define hyperparameters
	n_epochs = 50
	lr=0.001


	# Define Loss, Optimizer
	criterion = nn.CrossEntropyLoss()
	optimizer = torch.optim.Adam(model.parameters(), lr=lr)

	print("Début de l'Entraînement")

	# Training Run
	t1 = time.time()
	for epoch in range(1, n_epochs):
		optimizer.zero_grad() # Clears existing gradients from previous epoch
		#input_sample, target_sample = sample_seq(batch_len, batch_size, input_seq, target_seq)
		output, hidden = model(input_seq)
		loss = criterion(output, target_seq.view(-1).long())

		loss.backward() # Does backpropagation and calculates gradients
		optimizer.step() # Updates the weights accordingly
		
		if epoch%1 == 0:
			t2 = time.time()-t1
			t1 = time.time()
			print('Epoch: {}/{}.............'.format(epoch, n_epochs), end=' ')
			print("Loss: {:.4f}   {:.4f}".format(loss.item(), t2))

        # ICI ON RECUPERE LES PARAMETRES CONCERNANT LE NOMBRE DE MORCEAUX, LA DUREE, ETC
	
	print("Entraînement fini, génération des morceaux")

	out = [sample(model, 200, "360:p:76 ")] # on retourne le résultat sous la forme d'une liste

	print(out)

	# /!\ Attention, il faut couper la sortie en enlevant les triplets non complets !!

	return out
