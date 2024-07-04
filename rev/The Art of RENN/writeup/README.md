# Writeup

## TL;DR

There are 2 ways since this is a custom neural network model that only has a sequential linear model.

This means we can use `z3` to use a **Real** datatype and treat it as a matrix multiplication and addition bias of each layer.

Weight matrix is defined as :

$$W^{[l]} \in \mathbb{R}^{n^{[l]} \times n^{[l-1]}}$$

Bias vector is defined as :

$$b^{[l]} \in \mathbb{R}^{n^{[l]}}$$

In terms of layer of NN, 

$$y^{[1]} = W^{[1]} X + b^{[1]}$$

Since there are 3 layers, substitute it to `W` matrix later on.

The other way is to inverse the algorithm.

References:

* https://www.youtube.com/watch?v=aircAruvnKk&pp=ygUVbmV1cmFsIG5ldHdvcmsgcHl0aG9u
* https://www.youtube.com/watch?v=w8yWXqWQYmU&t=284s&pp=ygUVbmV1cmFsIG5ldHdvcmsgcHl0aG9u (Inspiration idea :) )