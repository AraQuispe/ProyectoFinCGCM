import threading

import cv2


class VideoCamara(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()

        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        print("GA")
        # 1.Conversion a Escala de Grises
        gray = cv2.cvtColor(camera.frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Escala de Grises sin filtro",gray)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        # cv2.imshow("Escala de Grises",gray)

        # 2.Deteccion de bordes
        edged = cv2.Canny(gray, 50, 150)
        # cv2.imshow("Edged",edged)

        # 3.Operaciones Morfologicas Cierre
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel, iterations=2)

        # 4.Encontrar contornos
        cnts, _ = cv2.findContours(closed.copy(),
                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # print "contornos",len(cnts)

        total = 0
        for c in cnts:

            area = cv2.contourArea(c)
            # print "area",area

            if area > 1700:

                # aproximacion de contorno
                peri = cv2.arcLength(c, True)  # Perimetro
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                # Si la aproximacion tiene 4 vertices correspondera a un rectangulo (Libro)
                if len(approx) == 4:
                    cv2.drawContours(camera.frame, [approx], -1, (0, 255, 0), 3, cv2.LINE_AA)
                    total += 1

        # 5.Poner texto en imagen
        letrero = 'Objetos: ' + str(total)
        cv2.putText(camera.frame, letrero, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        try:
            frame = camera.get_frame()
            yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg  \r\n\r\n' + frame +
                    b'\r\n\r\n')
        except:
            camera.__del__()
