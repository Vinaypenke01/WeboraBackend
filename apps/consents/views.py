import csv
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Consent
from .serializers import ConsentSerializer, ConsentCreateSerializer

class ConsentViewSet(viewsets.ModelViewSet):
    queryset = Consent.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ConsentCreateSerializer
        return ConsentSerializer

    def perform_create(self, serializer):
        consent = serializer.save()
        # 1. Notify Admin
        self.send_admin_notification(consent)
        # 2. Send simple "Success" email to Client (No PDF yet)
        self.send_client_confirmation(consent)

    def send_admin_notification(self, consent):
        from django.core.mail import EmailMessage
        from django.conf import settings
        
        subject = f"New Client Consent Submitted: {consent.full_name}"
        body = f"A new client consent has been submitted.\n\nClient: {consent.full_name}\nBusiness: {consent.business_name}\nEmail: {consent.email}\nMobile: {consent.mobile_number}\n\nPlease review it in the admin panel."
        
        try:
            email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
            email.send(fail_silently=True)
        except Exception as e:
            print(f"Error sending admin notification: {e}")

    def send_client_confirmation(self, consent):
        from django.core.mail import EmailMessage
        from django.conf import settings
        
        subject = f"Consent Received - {consent.business_name}"
        body = f"Dear {consent.full_name},\n\nWe have received your consent for our freelance services. Our team will review the details and finalize the agreement soon.\n\nYou will receive a copy of the final agreement once it is processed.\n\nBest regards,\nDigital Core Team"
        
        try:
            email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [consent.email])
            email.send(fail_silently=True)
        except Exception as e:
            print(f"Error sending client confirmation: {e}")

    def get_deployment_datetime(self, consent):
        from django.utils.dateparse import parse_date, parse_datetime
        from django.utils import timezone
        from datetime import datetime, date
        
        d_date = consent.deployment_date
        if not d_date:
            return consent.action_date if consent.action_date else consent.created_at
            
        if isinstance(d_date, str):
            parsed = parse_datetime(d_date) or parse_date(d_date)
            if parsed:
                d_date = parsed
        
        # Convert date to datetime if needed
        if isinstance(d_date, date) and not isinstance(d_date, datetime):
            d_date = datetime.combine(d_date, datetime.min.time())
            
        # Make timezone aware if naive
        if isinstance(d_date, datetime) and timezone.is_naive(d_date):
            return timezone.make_aware(d_date)
            
        return d_date

    def send_final_pdf_email(self, consent):
        from django.core.mail import EmailMessage
        from django.conf import settings
        
        # Ensure deployment_date is a datetime object for formatting
        d_date = self.get_deployment_datetime(consent)

        subject = f"Final Agreement - {consent.business_name}"
        body = f"Dear {consent.full_name},\n\nYour consent has been successfully processed and verified. Please find the finalized Terms and Conditions Agreement attached for your records.\n\nMaintenance Coverage: From {d_date.strftime('%B %d, %Y')} to {d_date.replace(year=d_date.year + 1).strftime('%B %d, %Y')}.\n\nBest regards,\nDigital Core Team"
        
        try:
            email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [consent.email])
            pdf_content = self.generate_pdf_content(consent)
            if pdf_content:
                filename = f"Consent_{consent.full_name.replace(' ', '_')}.pdf"
                email.attach(filename, pdf_content, 'application/pdf')
                email.send(fail_silently=False)  # Don't fail silently here to catch errors
                
                consent.is_final_email_sent = True
                consent.final_email_sent_at = timezone.now()
                consent.save()
                return True
            raise ValueError("PDF Generation failed - result was None. Check server logs for PDF GENERATION ERROR.")
        except Exception as e:
            import traceback
            error_msg = f"ERROR sending final PDF email: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            raise Exception(error_msg) # Re-raise to be caught by the action's try/except

    def generate_pdf_content(self, consent):
        import base64
        import os
        from io import BytesIO
        from xhtml2pdf import pisa
        from apps.site_settings.models import SiteSetting
        from django.conf import settings as django_settings
        
        db_settings = SiteSetting.objects.first()
        freelancer_name = db_settings.companyName if db_settings else "Digital Core"
        effective_date = consent.created_at.strftime("%B %d, %Y")
        
        # Calculate Maintenance Period
        deployment_date_obj = self.get_deployment_datetime(consent)
        expiry_date_obj = deployment_date_obj.replace(year=deployment_date_obj.year + 1)
        
        deployment_date = deployment_date_obj.strftime("%B %d, %Y")
        expiry_date = expiry_date_obj.strftime("%B %d, %Y")

        # Logo handling: convert to base64
        # Try multiple potential paths for production resilience
        possible_logo_paths = [
            os.path.join(django_settings.BASE_DIR.parent, 'Webora-Frontend', 'src', 'assets', 'logo.png'),
            os.path.join(django_settings.BASE_DIR, 'assets', 'logo.png'),
            os.path.join(django_settings.BASE_DIR, 'logo.png'),
            '/home/digitalcore/Webora-Frontend/src/assets/logo.png', # Potential PA path
        ]
        
        logo_path = None
        for p in possible_logo_paths:
            if os.path.exists(p):
                logo_path = p
                break

        logo_base64 = ""
        if logo_path:
            try:
                with open(logo_path, "rb") as image_file:
                    logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')
            except Exception as e:
                print(f"Error encoding logo: {e}")
        else:
            print("Logo not found in any expected location.")

        html_template = f"""
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <style>
                @page {{ size: a4 portrait; margin: 2cm; }}
                body {{ font-family: Helvetica, Arial, sans-serif; color: #333; line-height: 1.5; font-size: 10pt; }}
                .header {{ text-align: center; border-bottom: 2px solid #0056b3; padding-bottom: 10px; margin-bottom: 20px; }}
                .logo {{ height: 60px; margin-bottom: 10px; }}
                h1 {{ color: #0056b3; font-size: 18pt; margin: 0; text-transform: uppercase; }}
                h2 {{ color: #0056b3; font-size: 14pt; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 20px; }}
                .meta-table {{ width: 100%; margin-bottom: 20px; }}
                .meta-table td {{ padding: 5px 0; }}
                .label {{ font-weight: bold; width: 120px; }}
                .parties-section {{ background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .period-box {{ background-color: #eef6ff; padding: 10px; border-left: 4px solid #0056b3; margin: 20px 0; }}
                .footer-sign {{ margin-top: 50px; width: 100%; }}
                .signature-box {{ border-top: 1px solid #333; margin-top: 40px; padding-top: 5px; width: 250px; }}
            </style>
        </head>
        <body>
            <div class="header">
                {f'<img class="logo" src="data:image/png;base64,{logo_base64}">' if logo_base64 else ''}
                <h1>Terms and Conditions Agreement</h1>
                <p><strong>Freelance Web Development and Maintenance Services</strong></p>
            </div>

            <div class="parties-section">
                <p>This Agreement is made on this <strong>{consent.created_at.strftime("%d")} day of {consent.created_at.strftime("%B")}, {consent.created_at.year}</strong> ("Effective Date"), by and between:</p>
                <table class="meta-table">
                    <tr><td class="label">Freelancer:</td><td>{freelancer_name}</td></tr>
                    <tr><td class="label">Client:</td><td>{consent.full_name} ({consent.business_name})</td></tr>
                    <tr><td class="label">Terms Version:</td><td>v{consent.version_number}</td></tr>
                </table>
            </div>

            <div class="period-box">
                <strong>SERVICE MAINTENANCE PERIOD:</strong><br/>
                From: <strong>{deployment_date}</strong> (Deployment Date)<br/>
                To: <strong>{expiry_date}</strong> (One Year Coverage)
            </div>

            <div class="content">
                <h2>1. DEFINITIONS</h2>
                <p>"Services" shall mean the design, development, deployment, and maintenance of the website. "Deliverables" shall mean all outputs provided by the Freelancer to the Client. "Maintenance Period" shall mean the period of one (1) year commencing from the date of deployment.</p>
                <h2>2. SCOPE OF SERVICES</h2>
                <p>2.1 The Freelancer agrees to provide website design and development services. 2.2 Any services not expressly included shall be deemed "Additional Services".</p>
                <h2>3. PROJECT DELIVERY AND ACCEPTANCE</h2>
                <p>3.1 The Deliverables shall be deemed accepted upon deployment or written confirmation. 3.2 Objections must be communicated prior to deployment.</p>
                <h2>4. MAINTENANCE SERVICES</h2>
                <p>4.1 One (1) year maintenance starting from {deployment_date}. 4.2 Includes: Bug fixes, content updates, UI adjustments.</p>
                <h2>5. CHANGE REQUEST POLICY</h2>
                <p>5.1 Two changes per month. Minor modifications only.</p>
                <h2>6. TURNAROUND TIME</h2>
                <p>6.1 We strive for excellence and efficiency. The standard turnaround time for minor change requests or bug fixes is 2 to 5 business days.</p>
                <h2>7. INTELLECTUAL PROPERTY</h2>
                <p>7.1 Upon full and final payment, all rights, title, and interest in the Deliverables shall be transferred to the Client. 7.2 The Freelancer retains the right to use the Deliverables in their portfolio for promotional purposes.</p>
                <h2>8. CONFIDENTIALITY</h2>
                <p>8.1 Both parties agree to keep all project-related information, business secrets, and personal data confidential and not disclose it to any third party without prior written consent.</p>
                <h2>9. LIMITATION OF LIABILITY</h2>
                <p>9.1 In no event shall the Freelancer be liable for any indirect, special, or consequential damages. Total liability under this Agreement shall not exceed the fees paid for the specific services.</p>
                <h2>10. TERMINATION</h2>
                <p>10.1 Either party may terminate this Agreement with 15 days' written notice. 10.2 Upon termination, the Client shall pay for all work completed up to the termination date.</p>
                <h2>11. GOVERNING LAW</h2>
                <p>11.1 This Agreement shall be governed by and construed in accordance with the laws of India.</p>
                <h2>15. ACCEPTANCE</h2>
                <p>By signing below, both Parties acknowledge that they have read, understood, and agreed to the terms and conditions set forth in this Agreement.</p>
            </div>

            <table class="footer-sign">
                <tr>
                    <td><div class="signature-box"><strong>Freelancer:</strong> {freelancer_name}<br/>Digitally Verified</div></td>
                    <td><div class="signature-box"><strong>Client:</strong> {consent.full_name}<br/>Digitally Consented ({consent.email})</div></td>
                </tr>
            </table>
        </body>
        </html>
        """
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_template.encode("utf-8")), result)
        if not pdf.err:
            return result.getvalue()
        return None

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request, pk=None):
        try:
            consent = self.get_object()
            
            deployment_date = request.data.get('deployment_date')
            if not deployment_date:
                return Response({"error": "Actual Deployment Date is required to accept consent."}, status=status.HTTP_400_BAD_REQUEST)

            consent.status = 'ACCEPTED'
            consent.accepted_by = request.user
            consent.action_date = timezone.now()
            consent.deployment_date = deployment_date
            consent.admin_notes = request.data.get('admin_notes', '')
            consent.save()
            
            # Send Final PDF to Client
            sent_status = self.send_final_pdf_email(consent)
            
            serializer = self.get_serializer(consent)
            return Response({
                "message": "Consent accepted successfully.",
                "email_sent": sent_status,
                "data": serializer.data
            })
        except Exception as e:
            import traceback
            print(f"CRITICAL ERROR in accept action: {str(e)}")
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def resend_agreement(self, request, pk=None):
        try:
            consent = self.get_object()
            if consent.status != 'ACCEPTED':
                return Response({"error": "Cannot resend agreement for a consent that hasn't been accepted yet."}, status=status.HTTP_400_BAD_REQUEST)
            
            sent_status = self.send_final_pdf_email(consent)
            if sent_status:
                return Response({"message": "Agreement email resent successfully."})
            else:
                return Response({"error": "Failed to send email. Please check your SMTP settings."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"RESEND ERROR: {str(e)}\n{error_details}")
            return Response({
                "error": str(e),
                "details": error_details if django_settings.DEBUG else "Check server logs for details."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="consents_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Full Name', 'Email', 'Mobile', 'Business Name', 
            'Consented', 'Created At', 'Status', 'Accepted By', 'Action Date'
        ])
        
        consents = self.get_queryset()
        for c in consents:
            writer.writerow([
                c.id, c.full_name, c.email, c.mobile_number, c.business_name,
                c.is_consented, c.created_at, c.status, 
                c.accepted_by.email if c.accepted_by else '', c.action_date
            ])
            
        return response

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def download_document(self, request, pk=None):
        consent = self.get_object()
        pdf_content = self.generate_pdf_content(consent)
        
        if pdf_content:
            response = HttpResponse(pdf_content, content_type='application/pdf')
            filename = f"Consent_{consent.full_name.replace(' ', '_')}_{consent.created_at.strftime('%Y%m%d')}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
            
        return HttpResponse("Error generating PDF", status=500)
