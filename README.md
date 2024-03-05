# Al-Reem-store

In this project, the Django framework was used to build an e-commerce. It provides a comfortable and enjoyable purchasing experience where the customer can browse all available goods or search for products based on their categories or names. she can also preview the product description, choose the appropriate size, and then add it to the cart. Modify the cart by adding or removing products.
Before the payment process,  review the order, confirm the address, and then pay using PayPal

## Demo
[al-reem store demo]()

## setup
First thing to do is to clone the repository
```
$ git clone https://github.com/Reem-degais/Al-Reem-store.git
$ cd  Al-Reem-store
```
Create a virtual environment to install dependencies in and activate it
```
$ python -m venv env
$ env/Scripts/Activate
```
Then install django
```
(env)$ pip install django
```
note:(env) in front of the prompt indicates that this terminal session operates in a virtual environment.

Finally
```
$ cd ecommerce
$ python manage.py runserver
```

And navigate to http://127.0.0.1:8000



