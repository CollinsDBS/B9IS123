document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const appointmentForm = document.getElementById('appointmentForm');
    const addProductForm = document.getElementById('addProductForm');
    const productList = document.getElementById('productList');
    const adminProductList = document.getElementById('adminProductList');
    const adminUserList = document.getElementById('adminUserList');
    const adminAppointmentList = document.getElementById('adminAppointmentList');
    const adminOrderList = document.getElementById('adminOrderList');
    const cartList = document.getElementById('cartList');
    const checkoutButton = document.getElementById('checkoutButton');
    const orderList = document.getElementById('orderList');
    const appointmentList = document.getElementById('appointmentList');
    const logoutButton = document.getElementById('logout');

    const getToken = () => {
        const tokenString = localStorage.getItem('token');
        return JSON.parse(tokenString);
    };

    const saveToken = (userToken) => {
        localStorage.setItem('token', JSON.stringify(userToken));
    };

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            console.log('Submitting login request:', { username, password });

            try {
                const response = await fetch('http://127.0.0.1:5000/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                console.log('Response:', response);

                if (response.ok) {
                    const data = await response.json();
                    console.log('Response data:', data);
                    localStorage.setItem('token', data.access_token);
                    alert('Login successful');
                } else {
                    const errorText = await response.text();
                    console.log('Error response text:', errorText);
                    alert('Login failed: ' + response.statusText);
                }
            } catch (error) {
                console.error('Error during login request:', error);
                alert('Login failed');
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            console.log('Submitting registration request:', { username, email, password });

            try {
                const response = await fetch('http://127.0.0.1:5000/api/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, email, password })
                });

                console.log('Response:', response);

                if (response.ok) {
                    alert('Registration successful');
                } else {
                    const errorText = await response.text();
                    console.log('Error response text:', errorText);
                    alert('Registration failed: ' + response.statusText);
                }
            } catch (error) {
                console.error('Error during registration request:', error);
                alert('Registration failed');
            }
        });
    }

    if (appointmentForm) {
        appointmentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const serviceType = document.getElementById('serviceType').value;
            const appointmentDate = document.getElementById('appointmentDate').value;

            console.log('Submitting appointment request:', { serviceType, appointmentDate });

            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://127.0.0.1:5000/api/appointments', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ serviceType, appointmentDate })
                });

                console.log('Response:', response);

                if (response.ok) {
                    alert('Appointment booked successfully');
                } else {
                    const errorText = await response.text();
                    console.log('Error response text:', errorText);
                    alert('Booking failed: ' + response.statusText);
                }
            } catch (error) {
                console.error('Error during booking request:', error);
                alert('Booking failed');
            }
        });
    }
    
    // Logout functionality
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            localStorage.removeItem('token');
            alert('Logged out successfully');
            window.location.href = 'login.html';
        });
    }

    // Admin add product
    if (addProductForm) {
        addProductForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(addProductForm);
            const token = localStorage.getItem('token');

            try {
                const response = await fetch('http://127.0.0.1:5000/api/products', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    body: formData
                });

                if (response.ok) {
                    alert('Product added successfully');
                    fetchAdminProducts();
                } else {
                    const errorText = await response.text();
                    console.log('Error response text:', errorText);
                    alert('Adding product failed: ' + response.statusText);
                }
            } catch (error) {
                console.error('Error adding product:', error);
                alert('Adding product failed');
            }
        });
    }

    // Fetch Admin Products
    async function fetchAdminProducts() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://127.0.0.1:5000/api/products', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const products = await response.json();
            adminProductList.innerHTML = products.map(product => `
                <tr>
                    <td>${product.name}</td>
                    <td>${product.description}</td>
                    <td>$${product.price}</td>
                    <td>${product.category}</td>
                    <td>${product.stock_quantity}</td>
                    <td><img src="${product.image_url}" alt="${product.name}" width="50"></td>
                </tr>
            `).join('');
        } catch (error) {
            console.error('Error fetching products', error);
        }
    }

    // Delete Product
    async function deleteProduct(productId) {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://127.0.0.1:5000/api/products/${productId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                alert('Product deleted successfully');
                fetchAdminProducts();
            } else {
                const errorText = await response.text();
                console.log('Error response text:', errorText);
                alert('Deleting product failed: ' + response.statusText);
            }
        } catch (error) {
            console.error('Error deleting product:', error);
            alert('Deleting product failed');
        }
    }

    // Fetch Admin Users
    async function fetchAdminUsers() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://127.0.0.1:5000/api/admin/users', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const users = await response.json();
            document.querySelector('#adminUserList tbody').innerHTML = users.map(user => `
                <tr>
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>${user.role}</td>
                    <td>
                        <button onclick="updateUser(${user.id})">Update</button>
                        <button onclick="deleteUser(${user.id})">Delete</button>
                    </td>
                </tr>
            `).join('');
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    }

    // Delete User
    async function deleteUser(userId) {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://127.0.0.1:5000/api/admin/users/${userId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                alert('User deleted successfully');
                fetchAdminUsers();
            } else {
                const errorText = await response.text();
                console.log('Error response text:', errorText);
                alert('Deleting user failed: ' + response.statusText);
            }
        } catch (error) {
            console.error('Error deleting user:', error);
            alert('Deleting user failed');
        }
    }

    // Fetch Admin Appointments
    async function fetchAdminAppointments() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://127.0.0.1:5000/api/admin/appointments', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const appointments = await response.json();
            document.querySelector('#adminAppointmentList tbody').innerHTML = appointments.map(appointment => `
                <tr>
                    <td>${appointment.id}</td>
                    <td>${appointment.service_type}</td>
                    <td>${appointment.appointment_date}</td>
                    <td>${appointment.status}</td>
                    <td>
                        <button onclick="deleteAppointment(${appointment.id})">Delete</button>
                    </td>
                </tr>
            `).join('');
        } catch (error) {
            console.error('Error fetching appointments:', error);
        }
    }

    // Delete Appointment
    async function deleteAppointment(appointmentId) {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://127.0.0.1:5000/api/admin/appointments/${appointmentId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            alert('Appointment deleted successfully');
            fetchAdminAppointments(); // Refresh the appointment list
        } catch (error) {
            console.error('Error deleting appointment:', error);
            alert('Failed to delete appointment');
        }
    }

    // Fetch Admin Orders
    async function fetchAdminOrders() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://127.0.0.1:5000/api/admin/orders', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const orders = await response.json();
            adminOrderList.innerHTML = orders.map(order => `
                <tr>
                    <td>${order.id}</td>
                    <td>${order.user_id}</td>
                    <td>${order.order_date}</td>
                    <td>${order.total_amount}</td>
                    <td>${order.status}</td>
                    <td>${order.items}</td>
                </tr>
            `).join('');
        } catch (error) {
            console.error('Error fetching admin orders', error);
        }
    }

    

    // Fetch Customer Products
    async function fetchProducts() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/products');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const products = await response.json();
            productList.innerHTML = products.map(product => `
                <li>
                    ${product.name} - $${product.price}
                    <img src="${product.image_url}" alt="${product.name}" width="100">
                    <input type="number" id="quantity-${product.id}" min="1" value="1">
                    <button onclick="buyNow(${product.id}, document.getElementById('quantity-${product.id}').value)">Buy Now</button>
                </li>
            `).join('');
        } catch (error) {
            console.error('Error fetching products', error);
        }
    }

    window.buyNow = async (productId, quantity) => {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                alert('You must be logged in to place an order.');
                return;
            }
    
            const productResponse = await fetch(`http://127.0.0.1:5000/api/products/${productId}`);
            if (!productResponse.ok) {
                throw new Error(`HTTP error! status: ${productResponse.status}`);
            }
            const product = await productResponse.json();
    
            const orderData = {
                items: JSON.stringify([{ product_id: product.id, quantity: quantity }]),
                total_amount: product.price * quantity
            };
    
            const orderResponse = await fetch('http://127.0.0.1:5000/api/orders', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(orderData)
            });
    
            if (!orderResponse.ok) {
                throw new Error(`HTTP error! status: ${orderResponse.status}`);
            }
    
            alert('Order placed successfully');
            fetchOrders(); // Fetch updated order list
        } catch (error) {
            console.error('Error placing order:', error);
            alert('Failed to place order');
        }
    };
    

    // View Product Details
    async function viewProduct(productId) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/products/${productId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const product = await response.json();
            alert(`Name: ${product.name}\nDescription: ${product.description}\nPrice: $${product.price}\nCategory: ${product.category}\nStock: ${product.stock_quantity}\nImage: ${product.image_url}`);
        } catch (error) {
            console.error('Error fetching product details', error);
        }
    }

    // Fetch Orders
    async function fetchOrders() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://127.0.0.1:5000/api/orders', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const orders = await response.json();
            document.getElementById('orderList').innerHTML = orders.map(order => `
                <li>
                    Order ID: ${order.id} - $${order.total_amount} - Status: ${order.status}
                </li>
            `).join('');
        } catch (error) {
            console.error('Error fetching orders:', error);
        }
    }

    // Fetch Cart
    async function fetchCart() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://127.0.0.1:5000/api/customer/cart', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const cart = await response.json();
            cartList.innerHTML = JSON.parse(cart.items).map(item => `
                <li>${item.name} - $${item.price}</li>
            `).join('');
        } catch (error) {
            console.error('Error fetching cart', error);
        }
    }

    // Fetch Appointments
    async function fetchAppointments() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://127.0.0.1:5000/api/customer/appointments', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const appointments = await response.json();
            appointmentList.innerHTML = appointments.map(appointment => `
                <li>${appointment.service_type} - ${appointment.appointment_date} - ${appointment.status}</li>
            `).join('');
        } catch (error) {
            console.error('Error fetching appointments', error);
        }
    }

    // Fetch products, cart, orders, and appointments for customers
    if (productList) {
        fetchProducts();
    }
    if (cartList) {
        fetchCart();
    }
    if (orderList) {
        fetchOrders();
    }
    if (appointmentList) {
        fetchAppointments();
    }

    // Fetch admin data
    if (adminProductList) {
        fetchAdminProducts();
    }
    if (adminUserList) {
        fetchAdminUsers();
    }
    if (adminAppointmentList) {
        fetchAdminAppointments();
    }
    if (adminOrderList) {
        fetchAdminOrders();
    }
});
