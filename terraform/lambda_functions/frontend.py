

import json
import os
import base64

def lambda_handler(event, context):
    """
    Frontend Lambda function to serve the Poli Notary website
    """
    
    # Get the request path
    path = event.get('path', '/')
    http_method = event.get('httpMethod', 'GET')
    
    # CORS headers
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    # Handle OPTIONS requests for CORS
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': ''
        }
    
    # Serve static files based on path
    if path == '/' or path == '/index.html':
        return serve_html_page(cors_headers)
    elif path == '/styles.css':
        return serve_css(cors_headers)
    elif path == '/script.js':
        return serve_js(cors_headers)
    elif path.startswith('/assets/'):
        return serve_asset(path, cors_headers)
    else:
        # Default to serving the main page for SPA routing
        return serve_html_page(cors_headers)

def serve_html_page(cors_headers):
    """Serve the main HTML page"""
    
    s3_bucket = os.environ.get('S3_BUCKET', 'poli-notary-assets')
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poli Notary - Professional Notary Services</title>
    <link rel="stylesheet" href="/styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <i class="fas fa-stamp"></i>
                <span>Poli Notary</span>
            </div>
            <ul class="nav-menu">
                <li><a href="#home" class="nav-link">Home</a></li>
                <li><a href="#services" class="nav-link">Services</a></li>
                <li><a href="#about" class="nav-link">About</a></li>
                <li><a href="#contact" class="nav-link">Contact</a></li>
                <li><a href="#appointment" class="nav-link cta-button">Book Appointment</a></li>
            </ul>
            <div class="hamburger">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="hero-container">
            <div class="hero-content">
                <h1>Professional Notary Services You Can Trust</h1>
                <p>Certified, reliable, and convenient notarization services for all your legal document needs. Available 7 days a week with mobile services.</p>
                <div class="hero-buttons">
                    <a href="#appointment" class="btn btn-primary">Book Now</a>
                    <a href="#services" class="btn btn-secondary">Our Services</a>
                </div>
                <div class="hero-features">
                    <div class="feature">
                        <i class="fas fa-clock"></i>
                        <span>Same Day Service</span>
                    </div>
                    <div class="feature">
                        <i class="fas fa-mobile-alt"></i>
                        <span>Mobile Notary</span>
                    </div>
                    <div class="feature">
                        <i class="fas fa-shield-alt"></i>
                        <span>Fully Insured</span>
                    </div>
                </div>
            </div>
            <div class="hero-image">
                <img src="https://{s3_bucket}.s3.amazonaws.com/assets/images/notary-professional.jpg" alt="Professional Notary" class="hero-img">
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section id="services" class="services">
        <div class="container">
            <div class="section-header">
                <h2>Our Notary Services</h2>
                <p>Comprehensive notarization services for individuals and businesses</p>
            </div>
            <div class="services-grid">
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-file-signature"></i>
                    </div>
                    <h3>Document Notarization</h3>
                    <p>Acknowledgments, jurats, and copy certifications for legal documents, contracts, and affidavits.</p>
                    <img src="https://{s3_bucket}.s3.amazonaws.com/assets/images/document-signing.jpg" alt="Document Signing" class="service-img">
                </div>
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-home"></i>
                    </div>
                    <h3>Real Estate Services</h3>
                    <p>Specialized notary services for real estate transactions, refinancing, and property transfers.</p>
                    <img src="https://{s3_bucket}.s3.amazonaws.com/assets/images/real-estate.jpg" alt="Real Estate Services" class="service-img">
                </div>
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-car"></i>
                    </div>
                    <h3>Mobile Notary</h3>
                    <p>We come to you! Convenient mobile notary services at your home, office, or preferred location.</p>
                    <img src="https://{s3_bucket}.s3.amazonaws.com/assets/images/mobile-service.jpg" alt="Mobile Notary Service" class="service-img">
                </div>
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-briefcase"></i>
                    </div>
                    <h3>Business Services</h3>
                    <p>Corporate notarization services for business documents, contracts, and legal paperwork.</p>
                    <img src="https://{s3_bucket}.s3.amazonaws.com/assets/images/business-documents.jpg" alt="Business Services" class="service-img">
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="about">
        <div class="container">
            <div class="about-content">
                <div class="about-text">
                    <h2>About Poli Notary</h2>
                    <p class="lead">With over 10 years of experience in notary services, Poli Notary has been serving the community with professional, reliable, and convenient notarization services.</p>
                    <p>As a state-certified notary public, I am committed to providing accurate, efficient, and confidential notary services. Whether you need a simple document notarized or require complex real estate signing services, I ensure every detail is handled with the utmost professionalism.</p>
                    
                    <div class="credentials">
                        <h3>Credentials & Certifications</h3>
                        <div class="credential-list">
                            <div class="credential">
                                <i class="fas fa-certificate"></i>
                                <span>State Certified Notary Public</span>
                            </div>
                            <div class="credential">
                                <i class="fas fa-shield-alt"></i>
                                <span>$100,000 Surety Bond</span>
                            </div>
                            <div class="credential">
                                <i class="fas fa-lock"></i>
                                <span>E&O Insurance Coverage</span>
                            </div>
                            <div class="credential">
                                <i class="fas fa-graduation-cap"></i>
                                <span>Certified Loan Signing Agent</span>
                            </div>
                        </div>
                    </div>

                    <div class="stats">
                        <div class="stat">
                            <h4>5000+</h4>
                            <p>Documents Notarized</p>
                        </div>
                        <div class="stat">
                            <h4>10+</h4>
                            <p>Years Experience</p>
                        </div>
                        <div class="stat">
                            <h4>24/7</h4>
                            <p>Emergency Service</p>
                        </div>
                        <div class="stat">
                            <h4>100%</h4>
                            <p>Client Satisfaction</p>
                        </div>
                    </div>
                </div>
                <div class="about-image">
                    <img src="https://{s3_bucket}.s3.amazonaws.com/assets/images/notary-portrait.jpg" alt="Professional Notary Portrait" class="about-img">
                </div>
            </div>
        </div>
    </section>

    <!-- Testimonials Section -->
    <section class="testimonials">
        <div class="container">
            <div class="section-header">
                <h2>What Our Clients Say</h2>
                <p>Trusted by hundreds of satisfied customers</p>
            </div>
            <div class="testimonials-grid">
                <div class="testimonial-card">
                    <div class="client-photo">
                        <img src="https://{s3_bucket}.s3.amazonaws.com/assets/images/client-1.jpg" alt="Sarah Johnson">
                    </div>
                    <div class="stars">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                    </div>
                    <p>"Excellent service! Poli came to my home for a real estate signing and was incredibly professional and thorough. Made the whole process stress-free."</p>
                    <div class="client">
                        <strong>Sarah Johnson</strong>
                        <span>Real Estate Client</span>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="client-photo">
                        <img src="https://{s3_bucket}.s3.amazonaws.com/assets/images/client-2.jpg" alt="Michael Chen">
                    </div>
                    <div class="stars">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                    </div>
                    <p>"Fast, reliable, and convenient. I needed urgent notarization for business documents and Poli was able to accommodate same-day service. Highly recommended!"</p>
                    <div class="client">
                        <strong>Michael Chen</strong>
                        <span>Business Owner</span>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="client-photo">
                        <img src="https://{s3_bucket}.s3.amazonaws.com/assets/images/client-3.jpg" alt="Emily Rodriguez">
                    </div>
                    <div class="stars">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                    </div>
                    <p>"Professional and knowledgeable. Poli explained everything clearly and ensured all documents were properly notarized. Great experience overall."</p>
                    <div class="client">
                        <strong>Emily Rodriguez</strong>
                        <span>Individual Client</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact & Appointment Section -->
    <section id="contact" class="contact">
        <div class="container">
            <div class="contact-content">
                <div class="contact-info">
                    <h2>Get In Touch</h2>
                    <p>Ready to get your documents notarized? Contact us today to schedule an appointment or ask any questions.</p>
                    
                    <div class="contact-details">
                        <div class="contact-item">
                            <i class="fas fa-phone"></i>
                            <div>
                                <h4>Phone</h4>
                                <p>(555) 123-4567</p>
                            </div>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-envelope"></i>
                            <div>
                                <h4>Email</h4>
                                <p>info@polinotary.com</p>
                            </div>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-map-marker-alt"></i>
                            <div>
                                <h4>Service Area</h4>
                                <p>Greater Metropolitan Area<br>Mobile service available</p>
                            </div>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-clock"></i>
                            <div>
                                <h4>Hours</h4>
                                <p>Mon-Fri: 8AM-8PM<br>Sat-Sun: 9AM-6PM<br>Emergency: 24/7</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="appointment" class="appointment-form">
                    <h3>Book Your Appointment</h3>
                    <form class="contact-form" id="appointmentForm">
                        <div class="form-group">
                            <input type="text" name="fullName" placeholder="Full Name" required>
                        </div>
                        <div class="form-group">
                            <input type="email" name="email" placeholder="Email Address" required>
                        </div>
                        <div class="form-group">
                            <input type="tel" name="phone" placeholder="Phone Number" required>
                        </div>
                        <div class="form-group">
                            <select name="serviceType" required>
                                <option value="">Select Service Type</option>
                                <option value="standard">Standard Notarization</option>
                                <option value="mobile">Mobile Notary Service</option>
                                <option value="real-estate">Real Estate Signing</option>
                                <option value="business">Business Documents</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <input type="date" name="preferredDate" required>
                        </div>
                        <div class="form-group">
                            <select name="preferredTime" required>
                                <option value="">Preferred Time</option>
                                <option value="morning">Morning (8AM-12PM)</option>
                                <option value="afternoon">Afternoon (12PM-5PM)</option>
                                <option value="evening">Evening (5PM-8PM)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <textarea name="additionalDetails" placeholder="Additional Details (number of documents, location, etc.)" rows="4"></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Book Appointment</button>
                    </form>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <div class="footer-logo">
                        <i class="fas fa-stamp"></i>
                        <span>Poli Notary</span>
                    </div>
                    <p>Professional notary services you can trust. Licensed, bonded, and insured for your peace of mind.</p>
                    <div class="social-links">
                        <a href="#"><i class="fab fa-facebook"></i></a>
                        <a href="#"><i class="fab fa-linkedin"></i></a>
                        <a href="#"><i class="fab fa-google"></i></a>
                    </div>
                </div>
                <div class="footer-section">
                    <h4>Services</h4>
                    <ul>
                        <li><a href="#services">Document Notarization</a></li>
                        <li><a href="#services">Mobile Notary</a></li>
                        <li><a href="#services">Real Estate Signings</a></li>
                        <li><a href="#services">Business Services</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="#about">About Us</a></li>
                        <li><a href="#contact">Contact</a></li>
                        <li><a href="#appointment">Book Appointment</a></li>
                        <li><a href="#">Privacy Policy</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Contact Info</h4>
                    <p><i class="fas fa-phone"></i> (555) 123-4567</p>
                    <p><i class="fas fa-envelope"></i> info@polinotary.com</p>
                    <p><i class="fas fa-clock"></i> Available 7 Days a Week</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Poli Notary. All rights reserved. Licensed Notary Public.</p>
            </div>
        </div>
    </footer>

    <script src="/script.js"></script>
</body>
</html>
    """
    
    return {
        'statusCode': 200,
        'headers': {
            **cors_headers,
            'Content-Type': 'text/html'
        },
        'body': html_content
    }

def serve_css(cors_headers):
    """Serve CSS styles"""
    
    css_content = """
/* Reset and Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    color: #333;
    overflow-x: hidden;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navigation */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    z-index: 1000;
    padding: 1rem 0;
    transition: all 0.3s ease;
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-logo {
    display: flex;
    align-items: center;
    font-size: 1.5rem;
    font-weight: 700;
    color: #2563eb;
}

.nav-logo i {
    margin-right: 0.5rem;
    font-size: 1.8rem;
}

.nav-menu {
    display: flex;
    list-style: none;
    align-items: center;
}

.nav-menu li {
    margin-left: 2rem;
}

.nav-link {
    text-decoration: none;
    color: #333;
    font-weight: 500;
    transition: color 0.3s ease;
    position: relative;
}

.nav-link:hover {
    color: #2563eb;
}

.cta-button {
    background: #2563eb;
    color: white !important;
    padding: 0.75rem 1.5rem;
    border-radius: 50px;
    transition: all 0.3s ease;
}

.cta-button:hover {
    background: #1d4ed8;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(37, 99, 235, 0.3);
}

/* Hero Section */
.hero {
    padding: 120px 0 80px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    min-height: 100vh;
    display: flex;
    align-items: center;
}

.hero-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
}

.hero-content h1 {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    line-height: 1.2;
}

.hero-content p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    margin-bottom: 3rem;
}

.btn {
    padding: 1rem 2rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    display: inline-block;
    border: none;
    cursor: pointer;
    font-size: 1rem;
}

.btn-primary {
    background: white;
    color: #2563eb;
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.btn-secondary {
    background: transparent;
    color: white;
    border: 2px solid white;
}

.btn-secondary:hover {
    background: white;
    color: #2563eb;
}

.hero-features {
    display: flex;
    gap: 2rem;
}

.feature {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.feature i {
    font-size: 1.2rem;
    color: #fbbf24;
}

.hero-img {
    width: 100%;
    max-width: 400px;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

/* Services Section */
.services {
    padding: 80px 0;
    background: #f9fafb;
}

.section-header {
    text-align: center;
    margin-bottom: 4rem;
}

.section-header h2 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 1rem;
}

.section-header p {
    font-size: 1.2rem;
    color: #6b7280;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.service-card {
    background: white;
    padding: 2.5rem;
    border-radius: 15px;
    box-shadow: 0 5px 25px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    text-align: center;
}

.service-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.service-icon {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.5rem;
}

.service-icon i {
    font-size: 2rem;
    color: white;
}

.service-card h3 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #1f2937;
}

.service-card p {
    color: #6b7280;
    margin-bottom: 1.5rem;
}

.service-img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 10px;
    margin-top: 1rem;
}

/* About Section */
.about {
    padding: 80px 0;
    background: white;
}

.about-content {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 4rem;
    align-items: center;
}

.about-text h2 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 1.5rem;
}

.lead {
    font-size: 1.3rem;
    color: #2563eb;
    font-weight: 500;
    margin-bottom: 1.5rem;
}

.about-text p {
    color: #6b7280;
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
}

.credentials {
    margin: 2rem 0;
}

.credentials h3 {
    font-size: 1.3rem;
    color: #1f2937;
    margin-bottom: 1rem;
}

.credential-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
}

.credential {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    background: #f3f4f6;
    border-radius: 10px;
}

.credential i {
    color: #2563eb;
    font-size: 1.2rem;
}

.stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
    margin-top: 2rem;
}

.stat {
    text-align: center;
}

.stat h4 {
    font-size: 2rem;
    font-weight: 700;
    color: #2563eb;
    margin-bottom: 0.5rem;
}

.stat p {
    color: #6b7280;
    font-weight: 500;
}

.about-img {
    width: 100%;
    max-width: 400px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

/* Testimonials */
.testimonials {
    padding: 80px 0;
    background: #f9fafb;
}

.testimonials-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
}

.testimonial-card {
    background: white;
    padding: 2.5rem;
    border-radius: 15px;
    box-shadow: 0 5px 25px rgba(0, 0, 0, 0.08);
    text-align: center;
}

.client-photo {
    width: 80px;
    height: 80px;
    margin: 0 auto 1rem;
    border-radius: 50%;
    overflow: hidden;
}

.client-photo img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.stars {
    color: #fbbf24;
    margin-bottom: 1rem;
}

.testimonial-card p {
    font-style: italic;
    color: #4b5563;
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
}

.client strong {
    color: #1f2937;
    font-weight: 600;
}

.client span {
    color: #6b7280;
    font-size: 0.9rem;
}

/* Contact Section */
.contact {
    padding: 80px 0;
    background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
    color: white;
}

.contact-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
}

.contact-info h2 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
}

.contact-info p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.contact-details {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.contact-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}

.contact-item i {
    font-size: 1.5rem;
    color: #3b82f6;
    margin-top: 0.25rem;
}

.contact-item h4 {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
}

.contact-item p {
    opacity: 0.8;
    margin: 0;
}

.appointment-form {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 2.5rem;
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.appointment-form h3 {
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    text-align: center;
}

.contact-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    font-size: 1rem;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
    color: rgba(255, 255, 255, 0.7);
}

/* Footer */
.footer {
    background: #1f2937;
    color: white;
    padding: 3rem 0 1rem;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-logo {
    display: flex;
    align-items: center;
    font-size: 1.5rem;
    font-weight: 700;
    color: #3b82f6;
    margin-bottom: 1rem;
}

.footer-logo i {
    margin-right: 0.5rem;
    font-size: 1.8rem;
}

.footer-section p {
    opacity: 0.8;
    margin-bottom: 1rem;
}

.footer-section h4 {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #3b82f6;
}

.footer-section ul {
    list-style: none;
}

.footer-section li {
    margin-bottom: 0.5rem;
}

.footer-section a {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    transition: color 0.3s ease;
}

.footer-section a:hover {
    color: #3b82f6;
}

.social-links {
    display: flex;
    gap: 1rem;
}

.social-links a {
    width: 40px;
    height: 40px;
    background: #374151;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.social-links a:hover {
    background: #3b82f6;
    transform: translateY(-2px);
}

.footer-bottom {
    border-top: 1px solid #374151;
    padding-top: 1rem;
    text-align: center;
    opacity: 0.8;
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero-container {
        grid-template-columns: 1fr;
        text-align: center;
        gap: 2rem;
    }

    .hero-content h1 {
        font-size: 2.5rem;
    }

    .about-content {
        grid-template-columns: 1fr;
        gap: 2rem;
    }

    .stats {
        grid-template-columns: repeat(2, 1fr);
    }

    .contact-content {
        grid-template-columns: 1fr;
        gap: 2rem;
    }

    .services-grid {
        grid-template-columns: 1fr;
    }

    .testimonials-grid {
        grid-template-columns: 1fr;
    }
}
    """
    
    return {
        'statusCode': 200,
        'headers': {
            **cors_headers,
            'Content-Type': 'text/css'
        },
        'body': css_content
    }

def serve_js(cors_headers):
    """Serve JavaScript functionality"""
    
    js_content = """
// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form submission handling
const contactForm = document.getElementById('appointmentForm');
if (contactForm) {
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });
        
        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formObject)
            });
            
            if (response.ok) {
                alert('Thank you for your appointment request! We will contact you within 24 hours to confirm your booking.');
                this.reset();
            } else {
                alert('There was an error submitting your request. Please try again or call us directly.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('There was an error submitting your request. Please try again or call us directly.');
        }
    });
}

// Navbar background change on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.15)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        }
    }
});

// Counter animation for stats
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start) + (element.textContent.includes('+') ? '+' : '');
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target + (element.textContent.includes('+') ? '+' : '');
        }
    }
    
    updateCounter();
}

// Initialize counter animations when stats section is visible
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat h4');
            statNumbers.forEach(stat => {
                const text = stat.textContent;
                const number = parseInt(text.replace(/\\D/g, ''));
                if (number) {
                    animateCounter(stat, number);
                }
            });
            statsObserver.unobserve(entry.target);
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const statsSection = document.querySelector('.stats');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }
});
    """
    
    return {
        'statusCode': 200,
        'headers': {
            **cors_headers,
            'Content-Type': 'application/javascript'
        },
        'body': js_content
    }

def serve_asset(path, cors_headers):
    """Serve static assets from S3"""
    
    # For now, return a placeholder response
    # In production, this would fetch from S3
    return {
        'statusCode': 404,
        'headers': cors_headers,
        'body': json.dumps({'error': 'Asset not found'})
    }

