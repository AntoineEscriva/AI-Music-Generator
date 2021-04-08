# !/usr/bin/python3
#coding: utf-8

import torch
from torch import nn
import numpy as np
import time
from math import ceil
import random


def triplets_to_notes(entree):
  sortie = []
  for a in entree:  
    notes = a.strip().split(" ") #on sépare les triplets (en enlevant les potentiels espaces de fin)
    notes = [note.split(":") for note in notes] #on éclate les triplets
    notes = [ [int(n[0]), int(n[1]), int(n[2])] for n in notes] #on caste les informations tirées des triplets en int
    sortie.append(notes)
  return sortie


def one_hot_encode_rythme(sequence, dict_size, seq_len, batch_size):
    # Creating a multi-dimensional array of zeros with the desired output shape
    features = np.zeros((batch_size, seq_len, dict_size), dtype=np.float32)
    
    # Replacing the 0 at the relevant character index with a 1 to represent that character
    for i in range(batch_size):
        for u in range(seq_len):
            features[i, u, sequence[i][u]] = 1
    return features


def one_hot_encode_melodie(sequence, dict_size, seq_len, batch_size):
  # sequence est un triplet d'entiers
    features = np.zeros((batch_size, seq_len, dict_size), dtype=np.float32)

    for i in range(batch_size):
        for u in range(seq_len):
            features[i, u] = np.array(sequence[i][u])
    return features

#return nb_samples samples from input_t & target_t
def sample_seq_rythme(nb_samples, total, input_t, target_t):
    indexes = np.random.randint(0, total-1, nb_samples)
    input_shape = input_t.size()
    target_shape = target_t.size()
    new_input = torch.randn((nb_samples, input_shape[1], input_shape[2]), dtype=torch.float32)
    new_target = torch.randn((nb_samples, target_shape[1]), dtype=torch.float32)

    for a in range(len(indexes)):
        new_input[a] = input_t[indexes[a]].detach().clone()
        new_target[a] = target_t[indexes[a]].detach().clone()
    return new_input.to(device), new_target.to(device)


#return nb_samples samples from input_t & target_t
def sample_seq_melodie(nb_samples, total, input_t, target_t):
    indexes = np.random.randint(0, total-1, nb_samples)
    input_shape = input_t.size()
    target_shape = target_t.size()
    new_input = torch.randn((nb_samples, input_shape[1], input_shape[2]), dtype=torch.float32)
    new_target = torch.randn((nb_samples, target_shape[1], input_shape[2]), dtype=torch.float32)

    for a in range(len(indexes)):
        new_input[a] = input_t[indexes[a]].detach().clone()
        new_target[a] = target_t[indexes[a]].detach().clone()
    return new_input.to(device), new_target.to(device)


class Model(nn.Module):
    def __init__(self, input_size, output_size, hidden_dim, n_layers):
        super(Model, self).__init__()

        # Defining some parameters
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        #Defining the layers
        # RNN Layer
        self.rnn = nn.RNN(input_size, hidden_dim, n_layers, batch_first=True) 
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
def predict_rythme(model, character):
    # One-hot encoding our input to fit into the model
    character = np.array([[char2int[c] for c in character]])
    character = one_hot_encode_rythme(character, dict_size, character.shape[1], 1)
    character = torch.from_numpy(character)
    character = character.to(device)
    
    out, hidden = model(character)

    prob = nn.functional.softmax(out[-1], dim=0).data
    # Taking the class with the highest probability score from the output
    char_ind = torch.max(prob, dim=0)[1].item()

    return int2char[char_ind], hidden


# This function takes the desired output length and input characters as arguments, returning the produced sentence
def sample_rythme(model, out_len, start):
    model.eval() # eval mode
    ## start = start.lower() # WHY ?
    # First off, run through the starting characters
    chars = [ch for ch in start]
    size = out_len - len(chars)
    # Now pass in the previous characters and get a new one
    for ii in range(size):
        char, h = predict_rythme(model, chars)
        chars.append(char)

    return ''.join(chars)


# This function takes in the model and character as arguments and returns the next character prediction and hidden state
def predict_melodie(model, character):
    # One-hot encoding our input to fit into the model
    character = triplets_to_notes(character)[0]
    character = one_hot_encode_melodie(character, dict_size, len(character), 1)
    character = torch.from_numpy(character)
    character = character.to(device)
    
    out, hidden = model(character)
    
    new_vec = out.detach().to('cpu').numpy()[0]
    new_vec = ":".join([str(int(elt)) for elt in new_vec])

    return new_vec, hidden

# This function takes the desired output length and input characters as arguments, returning the produced sentence
def sample_melodie(model, out_len, start):
    model.eval() # eval mode
    ## start = start.lower() # WHY ?
    # First off, run through the starting characters
    chars = [ch for ch in start]
    size = out_len - len(chars)
    # Now pass in the previous characters and get a new one
    for ii in range(size):
        char, h = predict_melodie(model, chars)
        chars.append(char)

    return ' '.join(chars)


def device_choice():
	# torch.cuda.is_available() checks and returns a Boolean True if a GPU is available, else it'll return False
	is_cuda = torch.cuda.is_available()

	# If we have a GPU available, we'll set our device to GPU. We'll use this device variable later in our code.
	
	if is_cuda:
		device = torch.device("cuda")
		print("GPU is available")
	else:
		device = torch.device("cpu")
		print("GPU not available, CPU used")
	return device


def training_file_number_choice(total):
	#retourne le nombre de fichiers qui seront utilisés pour l'entrainement du RNN mais pas pour les tests
	return ceil(total * 80/100) # 80% des fichiers sont utilisés pour l'entraînement


def training_file_choice(liste, nb):
	#retourne une liste composée des fichiers utilisées pour l'entraînement et des fichiers utilisés pour les tests
	L = [i for i in range(len(liste))] #liste d'index
	L_id = random.sample(L, nb) #sample de taille nb d'index
	training = [liste[i] for i in L_id] #liste de training
	test = [liste[i] for i in range(len(liste)) if i not in L_id] #liste de test
	return [training, test]

def decoupe_morceau(morceau, taille):
	#morceau est sous la forme d'un tableau
	#découpe un morceau en plusieurs sous-parties de longueur taille+1
	#si la longueur du morceau n'est pas un multiple de taille+1, la partie restante sera ignorée
	return [morceau[i:i+taille+1] for i in range(0,len(morceau)-taille, taille+1)]


# Partie RNN pour le rythme seulement
def rnn_rythme(input_list, param_list):
	global device, int2char, char2int, dict_size

	lr = float(param_list[0]) 		# taux d'apprentissage du RNN
	nb_epochs = int(param_list[1])	# nombre de cycles d'entraînement
	len_hidden_dim = int(param_list[2]) # taille de la dimension cachée
	nb_layers = int(param_list[3])	# nombre de couches
	seq_len = int(param_list[4])	# longueur d'une séquence
	is_batch = bool(param_list[5])	# entraînement sous forme de batch ou non
	batch_len = int(param_list[6])	# nombre de séquences dans un batch
	nb_morceaux = int(param_list[7])# nombre de morceaux à produire
	duree_morceaux = int(param_list[8]) #longueur des morceaux 
	# LA DUREE DES MORCEAUX EST DONNEE EN NOMBRE DE NOTES !
	# PAS EN SECONDES


	device = device_choice() #choix du device (CPU ou GPU)

	training_text = [] # liste des training files de longueur taille+1 que l'on va découper
	test_text = [] # liste des tests files de longueur taille+1 que l'on va découper 

	nb_training_files = training_file_number_choice(len(input_list))
	training_files, test_files = training_file_choice(input_list, nb_training_files)


	for i in training_files:
		training_text += decoupe_morceau(i, seq_len)


	for i in test_files:
		test_text += decoupe_morceau(i, seq_len)

	chars = set(''.join(training_text)).union(''.join(test_text)) # on joint les text et on extrait les caractères de manière unique
	int2char = dict(enumerate(chars)) # on crée un dictionnaire pour maper les entiers aux caractères
	char2int = {char: ind for ind, char in int2char.items()} 	# on crée un autre dictionnaire qui map les caractères aux entiers

	dict_size = len(char2int)	# taille du dictionnaire
	training_batch_size = len(training_text) # nombre de séquences de training
	test_batch_size = len(test_text) # nombre de séquences de test

	# Création des listes qui vont contenir les séquences de test et d'entraînement
	training_input_seq = []
	training_target_seq = []
	test_input_seq = []
	test_target_seq = []


	for i in range(training_batch_size):
		# Remove last character for input sequence
		training_input_seq.append(training_text[i][:-1])

		# Remove first character for target sequence
		training_target_seq.append(training_text[i][1:])

	for i in range(test_batch_size):
		# Remove last character for input sequence
		test_input_seq.append(test_text[i][:-1])

		# Remove first character for target sequence
		test_target_seq.append(test_text[i][1:])



	for i in range(training_batch_size):
		training_input_seq[i] = [char2int[char] for char in training_input_seq[i]]
		training_target_seq[i] = [char2int[char] for char in training_target_seq[i]]

	for i in range(test_batch_size):
		test_input_seq[i] = [char2int[char] for char in test_input_seq[i]]
		test_target_seq[i] = [char2int[char] for char in test_target_seq[i]]


	#encodage des input de training
	training_input_seq = one_hot_encode_rythme(training_input_seq, dict_size, seq_len, training_batch_size)

	training_input_seq = torch.from_numpy(training_input_seq)
	training_target_seq = torch.Tensor(training_target_seq)

	#encodage des input de test
	test_input_seq = one_hot_encode_rythme(test_input_seq, dict_size, seq_len, test_batch_size)

	test_input_seq = torch.from_numpy(test_input_seq)
	test_target_seq = torch.Tensor(test_target_seq)



	# on crée le modèle avec les hyperparamètres
	model = Model(input_size=dict_size, output_size=dict_size, hidden_dim=len_hidden_dim, n_layers=nb_layers)
	model = model.to(device) # on déplace le modèle vers le device utilisé

	# on déplace les input et target des tests et entraînements vers le device utilisé
	training_input_seq = training_input_seq.to(device) 
	training_target_seq = training_target_seq.to(device)
	test_input_seq = test_input_seq.to(device) 
	test_target_seq = test_target_seq.to(device)

	# définition de la fontcion d'erreur et de l'optimiseur
	criterion = nn.CrossEntropyLoss()
	optimizer = torch.optim.Adam(model.parameters(), lr=lr)

	print("Début de l'Entraînement")

	old_training_loss = 100
	old_test_loss = 100
	list_training_loss = []
	list_test_loss = []
	list_lr = []

	# Boucle d'entraînement
	t1 = time.time()
	for epoch in range(1, nb_epochs):
		optimizer.zero_grad() # on efface les gradients de l'entraînement précédent
		if (is_batch):
			# si on utilise des batch, alors on récupère une fraction des inputs et des targets
			training_input_sample, training_target_sample = sample_seq_rythme(batch_len, training_batch_size, training_input_seq, training_target_seq)
			output, hidden = model(training_input_sample)
			new_training_loss = criterion(output, training_target_sample.view(-1).long())
		else:
			output, hidden = model(training_input_seq)
			new_training_loss = criterion(output, training_target_seq.view(-1).long())

		new_training_loss.backward() # backpropagation et calcul du nouveau gradient
		optimizer.step() # mise à jour des poids
		
		if epoch%1 == 0:
			t2 = time.time()-t1
			t1 = time.time()
			print('Epoch: {}/{}.............'.format(epoch, nb_epochs), end=' ')
			print("Loss: {:.4f}   {:.4f}".format(new_training_loss.item(), t2))

			if(is_batch and test_batch_size != 0):
				test_input_sample, test_target_sample = sample_seq_rythme(batch_len, test_batch_size, test_input_seq, test_target_seq)
				output, hidden = model(test_input_sample)
				new_test_loss = criterion(output, test_target_sample.view(-1).long())
			else:
				output, hidden = model(test_input_seq)
				new_test_loss = criterion(output, test_target_seq.view(-1).long())

			if(new_test_loss < old_test_loss):
				print("Test sur les données de test \t Loss : {} BAISSE".format(new_test_loss.item()))
			else:
				print("Test sur les données de test \t Loss : {} AUGMENTATION".format(new_test_loss.item()))

			old_test_loss = new_test_loss
			list_test_loss.append(new_test_loss)

		old_training_loss = new_training_loss
		list_training_loss.append(new_training_loss)
		list_lr.append(lr)
		lr -= (1/100) * lr #mise à jour du learning rate
	
	print("Entraînement fini, génération des morceaux")

	# on retourne le résultat sous la forme d'une liste
	out = []
	for a in range(nb_morceaux):
		note_aleatoire = int2char[random.randint(0,len(int2char)-1)]
		out.append(sample_rythme(model, 100, note_aleatoire))

	return out


# Partie RNN pour le rythme et la mélodie

def rnn_rythme_melodie(input_list, param_list):
	global device, int2char, char2int, dict_size

	lr = float(param_list[0]) 		# taux d'apprentissage du RNN
	nb_epochs = int(param_list[1])	# nombre de cycles d'entraînement
	len_hidden_dim = int(param_list[2]) # taille de la dimension cachée
	nb_layers = int(param_list[3])	# nombre de couches
	seq_len = int(param_list[4])	# longueur d'une séquence
	is_batch = bool(param_list[5])	# entraînement sous forme de batch ou non
	batch_len = int(param_list[6])	# nombre de séquences dans un batch
	nb_morceaux = int(param_list[7])# nombre de morceaux à produire
	duree_morceaux = int(param_list[8]) #longueur des morceaux 
	# LA DUREE DES MORCEAUX EST DONNEE EN NOMBRE DE NOTES !
	# PAS EN SECONDES
	dict_size = 3

	input_list = triplets_to_notes(input_list) #on transforme la chaîne de triplets en liste de triplets

	device = device_choice() #choix du device (CPU ou GPU)

	#taille = 200 #longueur d'une séquence # de 100 à 200 généralement

	training_text = [] # liste des training files de longueur taille+1 que l'on va découper
	test_text = [] # liste des tests files de longueur taille+1 que l'on va découper 

	nb_training_files = training_file_number_choice(len(input_list))
	training_files, test_files = training_file_choice(input_list, nb_training_files)


	for i in training_files:
		training_text += decoupe_morceau(i, seq_len)
	
	for i in test_files:
		test_text += decoupe_morceau(i, seq_len)


	training_batch_size = len(training_text)
	test_batch_size = len(test_text)
	# Creating lists that will hold our input and target sequences
	training_input_seq = []
	training_target_seq = []
	test_input_seq = []
	test_target_seq = []


	for i in range(training_batch_size):
		# Remove last character for input sequence
		training_input_seq.append(training_text[i][:-1])

		# Remove first character for target sequence
		training_target_seq.append(training_text[i][1:])

	for i in range(test_batch_size):
		# Remove last character for input sequence
		test_input_seq.append(test_text[i][:-1])

		# Remove first character for target sequence
		test_target_seq.append(test_text[i][1:])


	# encodage des input et target de training
	training_input_seq = one_hot_encode_melodie(training_input_seq, dict_size, seq_len, training_batch_size)
	training_input_seq = torch.from_numpy(training_input_seq)
	training_target_seq = torch.Tensor(training_target_seq)

	# encodage des input et target de test
	test_input_seq = one_hot_encode_melodie(test_input_seq, dict_size, seq_len, test_batch_size)
	test_input_seq = torch.from_numpy(test_input_seq)
	test_target_seq = torch.Tensor(test_target_seq)



	# on crée le modèle avec les hyperparamètres
	model = Model(input_size=dict_size, output_size=dict_size, hidden_dim=len_hidden_dim, n_layers=nb_layers)
	model = model.to(device) # on déplace le modèle vers le device utilisé

	# on déplace les input et target des tests et entraînements vers le device utilisé
	training_input_seq = training_input_seq.to(device) 
	training_target_seq = training_target_seq.to(device)
	test_input_seq = test_input_seq.to(device) 
	test_target_seq = test_target_seq.to(device)

	# définition de la fontcion d'erreur et de l'optimiseur
	criterion = nn.L1Loss()
	optimizer = torch.optim.Adam(model.parameters(), lr=lr)

	print("Début de l'Entraînement")

	old_training_loss = 100
	old_test_loss = 100
	list_training_loss = []
	list_test_loss = []
	list_lr = []

	# Boucle d'entraînement
	t1 = time.time()
	for epoch in range(1, nb_epochs):
		optimizer.zero_grad() # on efface les gradients de l'entraînement précédent
		if (is_batch):
			training_input_sample, training_target_sample = sample_seq_melodie(batch_len, training_batch_size, training_input_seq, training_target_seq)
			output, hidden = model(training_input_sample)
			new_training_loss = criterion(output.view(-1), training_target_sample.view(-1).long())
		else:
			output, hidden = model(training_input_seq)
			new_training_loss = criterion(output.veiw(-1), training_target_seq.view(-1).long())

		new_training_loss.backward() # backpropagation et calcul du nouveau gradient
		optimizer.step() # mise à jour des poids
		
		if epoch%10 == 0:
			t2 = time.time()-t1
			t1 = time.time()
			print('Epoch: {}/{}.............'.format(epoch, nb_epochs), end=' ')
			print("Loss: {:.4f}   {:.4f}".format(new_training_loss.item(), t2))

			if(is_batch and test_batch_size != 0):
				test_input_sample, test_target_sample = sample_seq_melodie(batch_len, test_batch_size, test_input_seq, test_target_seq)
				output, hidden = model(test_input_sample)
				new_test_loss = criterion(output.view(-1), test_target_sample.view(-1).long())
			else:
				output, hidden = model(test_input_seq)
				new_test_loss = criterion(output.view(-1), test_target_seq.view(-1).long())

			if(new_test_loss < old_test_loss):
				print("Test sur les données de test \t Loss : {} BAISSE".format(new_test_loss.item()))
			else:
				print("Test sur les données de test \t Loss : {} AUGMENTATION".format(new_test_loss.item()))

			old_test_loss = new_test_loss
			list_test_loss.append(new_test_loss)

		old_training_loss = new_training_loss
		list_training_loss.append(new_training_loss)
		list_lr.append(lr)
	
	print("Entraînement fini, génération des morceaux")

	out = []
	for a in range(nb_morceaux):
		note_aleatoire = ["480:120:76"]
		out.append(sample_melodie(model, duree_morceaux, note_aleatoire))

	return out
