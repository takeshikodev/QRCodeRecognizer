import cv2
import numpy as np
from pyzbar.pyzbar import decode

class QRCodeDetector:
    """Class for detecting QR codes in images"""
    
    @staticmethod
    def detect_qr_codes(image):
        """
        Detects QR codes in an image using various processing techniques
        
        Args:
            image: OpenCV image
            
        Returns:
            list: List of found QR codes
            processed_image: Image with marked QR codes
        """
        results = []
        processed_image = image.copy()
        
        original_results = QRCodeDetector._decode_image(image)
        results.extend(original_results)
        
        if results:
            QRCodeDetector._mark_qr_codes(processed_image, original_results)
            return results, processed_image
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_results = QRCodeDetector._decode_image(gray)
        results.extend(gray_results)
        
        if results:
            QRCodeDetector._mark_qr_codes(processed_image, gray_results)
            return results, processed_image
        
        binary = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )
        binary_results = QRCodeDetector._decode_image(binary)
        results.extend(binary_results)
        
        if results:
            QRCodeDetector._mark_qr_codes(processed_image, binary_results)
            return results, processed_image
        
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        enhanced_results = QRCodeDetector._decode_image(enhanced)
        results.extend(enhanced_results)
        
        if results:
            QRCodeDetector._mark_qr_codes(processed_image, enhanced_results)
            
        if not results:
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            blurred_results = QRCodeDetector._decode_image(blurred)
            results.extend(blurred_results)
            
            if blurred_results:
                QRCodeDetector._mark_qr_codes(processed_image, blurred_results)
        
        if not results:
            edges = cv2.Canny(gray, 100, 200)
            dilated = cv2.dilate(edges, None, iterations=1)
            edge_results = QRCodeDetector._decode_image(dilated)
            results.extend(edge_results)
            
            if edge_results:
                QRCodeDetector._mark_qr_codes(processed_image, edge_results)
            
        return results, processed_image
    
    @staticmethod
    def _decode_image(image):
        """Decodes a QR code from an image"""
        try:
            return decode(image)
        except Exception:
            return []
    
    @staticmethod
    def _mark_qr_codes(image, qr_codes):
        """Marks QR codes on the image with frames and text"""
        for qr in qr_codes:
            points = qr.polygon
            if points:
                hull = cv2.convexHull(
                    np.array([(p.x, p.y) for p in points], dtype=np.int32)
                )
                cv2.polylines(
                    image, [hull], True, (0, 255, 0), 3
                )
                
                x = points[0].x
                y = points[0].y
                cv2.putText(
                    image, qr.type, (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
                ) 