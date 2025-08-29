


import json
import boto3
import os
import uuid
from datetime import datetime
from decimal import Decimal

# Initialize AWS services
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

def lambda_handler(event, context):
    """
    Backend Lambda function to handle API requests for Poli Notary website
    """
    
    # CORS headers
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    try:
        # Get request details
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        
        # Handle OPTIONS requests for CORS
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': ''
            }
        
        # Route requests
        if path == '/api/contact' and http_method == 'POST':
            return handle_contact_submission(event, cors_headers)
        elif path == '/api/contact' and http_method == 'GET':
            return get_contact_submissions(event, cors_headers)
        else:
            return {
                'statusCode': 404,
                'headers': cors_headers,
                'body': json.dumps({'error': 'Endpoint not found'})
            }
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': 'Internal server error'})
        }

def handle_contact_submission(event, cors_headers):
    """Handle contact form submission"""
    
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        required_fields = ['fullName', 'email', 'phone', 'serviceType']
        for field in required_fields:
            if not body.get(field):
                return {
                    'statusCode': 400,
                    'headers': cors_headers,
                    'body': json.dumps({'error': f'Missing required field: {field}'})
                }
        
        # Generate unique ID and timestamp
        submission_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Prepare data for DynamoDB
        submission_data = {
            'id': submission_id,
            'timestamp': timestamp,
            'fullName': body.get('fullName'),
            'email': body.get('email'),
            'phone': body.get('phone'),
            'serviceType': body.get('serviceType'),
            'preferredDate': body.get('preferredDate', ''),
            'preferredTime': body.get('preferredTime', ''),
            'additionalDetails': body.get('additionalDetails', ''),
            'status': 'new',
            'source': 'website'
        }
        
        # Save to DynamoDB
        table_name = os.environ.get('DYNAMODB_TABLE')
        if table_name:
            table = dynamodb.Table(table_name)
            table.put_item(Item=submission_data)
        
        # Send notification email
        send_notification_email(submission_data)
        
        # Send confirmation email to client
        send_confirmation_email(submission_data)
        
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({
                'message': 'Appointment request submitted successfully',
                'id': submission_id
            })
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    except Exception as e:
        print(f"Error handling contact submission: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': 'Failed to process submission'})
        }

def get_contact_submissions(event, cors_headers):
    """Get contact form submissions (for admin use)"""
    
    try:
        # This would typically require authentication
        # For demo purposes, we'll return a simple response
        
        table_name = os.environ.get('DYNAMODB_TABLE')
        if not table_name:
            return {
                'statusCode': 500,
                'headers': cors_headers,
                'body': json.dumps({'error': 'Database not configured'})
            }
        
        table = dynamodb.Table(table_name)
        
        # Get query parameters
        query_params = event.get('queryStringParameters') or {}
        limit = int(query_params.get('limit', 10))
        
        # Scan table (in production, you'd want better querying)
        response = table.scan(Limit=limit)
        
        # Convert Decimal to float for JSON serialization
        items = []
        for item in response.get('Items', []):
            converted_item = {}
            for key, value in item.items():
                if isinstance(value, Decimal):
                    converted_item[key] = float(value)
                else:
                    converted_item[key] = value
            items.append(converted_item)
        
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({
                'submissions': items,
                'count': len(items)
            })
        }
        
    except Exception as e:
        print(f"Error getting submissions: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': 'Failed to retrieve submissions'})
        }

def send_notification_email(submission_data):
    """Send notification email to Poli Notary"""
    
    try:
        subject = f"New Appointment Request - {submission_data['serviceType']}"
        
        body_html = f"""
        <html>
        <head></head>
        <body>
            <h2>New Appointment Request</h2>
            <p>You have received a new appointment request through your website.</p>
            
            <h3>Client Information:</h3>
            <ul>
                <li><strong>Name:</strong> {submission_data['fullName']}</li>
                <li><strong>Email:</strong> {submission_data['email']}</li>
                <li><strong>Phone:</strong> {submission_data['phone']}</li>
                <li><strong>Service Type:</strong> {submission_data['serviceType']}</li>
                <li><strong>Preferred Date:</strong> {submission_data.get('preferredDate', 'Not specified')}</li>
                <li><strong>Preferred Time:</strong> {submission_data.get('preferredTime', 'Not specified')}</li>
            </ul>
            
            <h3>Additional Details:</h3>
            <p>{submission_data.get('additionalDetails', 'None provided')}</p>
            
            <h3>Submission Details:</h3>
            <ul>
                <li><strong>Submission ID:</strong> {submission_data['id']}</li>
                <li><strong>Timestamp:</strong> {submission_data['timestamp']}</li>
                <li><strong>Source:</strong> {submission_data['source']}</li>
            </ul>
            
            <p>Please contact the client within 24 hours to confirm the appointment.</p>
        </body>
        </html>
        """
        
        body_text = f"""
        New Appointment Request
        
        Client Information:
        Name: {submission_data['fullName']}
        Email: {submission_data['email']}
        Phone: {submission_data['phone']}
        Service Type: {submission_data['serviceType']}
        Preferred Date: {submission_data.get('preferredDate', 'Not specified')}
        Preferred Time: {submission_data.get('preferredTime', 'Not specified')}
        
        Additional Details:
        {submission_data.get('additionalDetails', 'None provided')}
        
        Submission ID: {submission_data['id']}
        Timestamp: {submission_data['timestamp']}
        
        Please contact the client within 24 hours to confirm the appointment.
        """
        
        # Send email (you'll need to verify the email address in SES first)
        ses.send_email(
            Source='noreply@polinotary.com',  # This needs to be verified in SES
            Destination={
                'ToAddresses': ['info@polinotary.com']  # This needs to be verified in SES
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': body_html,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        
    except Exception as e:
        print(f"Error sending notification email: {str(e)}")
        # Don't fail the request if email fails

def send_confirmation_email(submission_data):
    """Send confirmation email to client"""
    
    try:
        subject = "Appointment Request Received - Poli Notary"
        
        body_html = f"""
        <html>
        <head></head>
        <body>
            <h2>Thank You for Your Appointment Request</h2>
            <p>Dear {submission_data['fullName']},</p>
            
            <p>Thank you for choosing Poli Notary for your notarization needs. We have received your appointment request and will contact you within 24 hours to confirm your booking.</p>
            
            <h3>Your Request Details:</h3>
            <ul>
                <li><strong>Service Type:</strong> {submission_data['serviceType']}</li>
                <li><strong>Preferred Date:</strong> {submission_data.get('preferredDate', 'Not specified')}</li>
                <li><strong>Preferred Time:</strong> {submission_data.get('preferredTime', 'Not specified')}</li>
                <li><strong>Reference ID:</strong> {submission_data['id']}</li>
            </ul>
            
            <h3>What's Next?</h3>
            <p>Our team will review your request and contact you at {submission_data['phone']} or {submission_data['email']} to:</p>
            <ul>
                <li>Confirm your appointment details</li>
                <li>Discuss any specific requirements</li>
                <li>Provide pricing information</li>
                <li>Answer any questions you may have</li>
            </ul>
            
            <h3>Need Immediate Assistance?</h3>
            <p>If you have an urgent request or need to speak with us immediately, please call us at (555) 123-4567.</p>
            
            <p>Thank you for choosing Poli Notary!</p>
            
            <p>Best regards,<br>
            The Poli Notary Team<br>
            (555) 123-4567<br>
            info@polinotary.com</p>
        </body>
        </html>
        """
        
        body_text = f"""
        Thank You for Your Appointment Request
        
        Dear {submission_data['fullName']},
        
        Thank you for choosing Poli Notary for your notarization needs. We have received your appointment request and will contact you within 24 hours to confirm your booking.
        
        Your Request Details:
        Service Type: {submission_data['serviceType']}
        Preferred Date: {submission_data.get('preferredDate', 'Not specified')}
        Preferred Time: {submission_data.get('preferredTime', 'Not specified')}
        Reference ID: {submission_data['id']}
        
        What's Next?
        Our team will review your request and contact you at {submission_data['phone']} or {submission_data['email']} to:
        - Confirm your appointment details
        - Discuss any specific requirements
        - Provide pricing information
        - Answer any questions you may have
        
        Need Immediate Assistance?
        If you have an urgent request or need to speak with us immediately, please call us at (555) 123-4567.
        
        Thank you for choosing Poli Notary!
        
        Best regards,
        The Poli Notary Team
        (555) 123-4567
        info@polinotary.com
        """
        
        # Send confirmation email to client
        ses.send_email(
            Source='noreply@polinotary.com',  # This needs to be verified in SES
            Destination={
                'ToAddresses': [submission_data['email']]
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': body_html,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        
    except Exception as e:
        print(f"Error sending confirmation email: {str(e)}")
        # Don't fail the request if email fails


