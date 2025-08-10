# ==============================================================================
# DROWSINESSGUARD: KODE PROGRAM UTAMA
# ==============================================================================
import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
from playsound import playsound
from threading import Thread

# --- KONSTANTA YANG DAPAT DISESUAIKAN (KALIBRASI) ---

# 1. Eye Aspect Ratio (EAR) Threshold
# Nilai EAR di bawah ini dianggap mata tertutup. Sesuaikan nilai ini.
# Turunkan jika alarm tidak sensitif, naikkan jika terlalu sensitif.
EAR_THRESHOLD = 0.22

# 2. Drowsy Frames Threshold
# Jumlah frame berturut-turut mata harus tertutup sebelum alarm berbunyi.
# (Contoh: 35 frame pada ~24 FPS adalah sekitar 1.5 detik)
DROWSY_FRAMES_THRESHOLD = 35

# --- VARIABEL GLOBAL & INISIALISASI ---

# Penghitung frame untuk kondisi mata tertutup
FRAME_COUNTER = 0
# Status alarm (True jika sedang berbunyi)
ALARM_ON = False
# Path ke file suara alarm
ALARM_SOUND_PATH = "alarm.wav"

# Inisialisasi MediaPipe Face Mesh untuk deteksi landmark wajah
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Indeks spesifik untuk landmark mata dari model MediaPipe
# Urutan: [titik horizontal 1, titik vertikal atas, titik vertikal bawah, 
#          titik horizontal 2, titik vertikal atas, titik vertikal bawah]
LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]

# --- FUNGSI-FUNGSI UTAMA ---

def calculate_ear(eye_landmarks):
    """
    Menghitung Eye Aspect Ratio (EAR) untuk satu mata.
    Rumus EAR: EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
    """
    # Menghitung jarak Euclidean vertikal
    p2_p6 = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
    p3_p5 = dist.euclidean(eye_landmarks[2], eye_landmarks[4])
    # Menghitung jarak Euclidean horizontal
    p1_p4 = dist.euclidean(eye_landmarks[0], eye_landmarks[3])
    
    # Menghitung EAR berdasarkan rumus
    ear = (p2_p6 + p3_p5) / (2.0 * p1_p4)
    return ear

def play_alarm(sound_path):
    """Memainkan suara alarm."""
    try:
        playsound(sound_path)
    except Exception as e:
        print(f"[ERROR] Gagal memutar suara alarm: {e}")

# --- PROGRAM UTAMA ---

print("[INFO] Memulai webcam...")
# Mengakses webcam utama (biasanya indeks 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[ERROR] Tidak bisa membuka webcam.")
    exit()

# Loop utama untuk memproses setiap frame dari video
while True:
    # Membaca frame dari webcam
    ret, frame = cap.read()
    if not ret:
        print("[INFO] Stream video berakhir. Menutup program.")
        break

    # 1. Pra-pemrosesan Frame
    frame = cv2.flip(frame, 1) # Balik frame secara horizontal (efek cermin)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Konversi warna ke RGB
    height, width, _ = frame.shape

    # 2. Deteksi Wajah dan Landmark
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        # Asumsi hanya ada satu wajah
        face_landmarks = results.multi_face_landmarks[0]
        
        # 3. Ekstrak Koordinat Mata dan Hitung EAR
        left_eye_coords = np.array([(int(face_landmarks.landmark[i].x * width), int(face_landmarks.landmark[i].y * height)) for i in LEFT_EYE_INDICES])
        right_eye_coords = np.array([(int(face_landmarks.landmark[i].x * width), int(face_landmarks.landmark[i].y * height)) for i in RIGHT_EYE_INDICES])
        
        left_ear = calculate_ear(left_eye_coords)
        right_ear = calculate_ear(right_eye_coords)
        
        # Rata-ratakan EAR dari kedua mata
        avg_ear = (left_ear + right_ear) / 2.0
        
        # 4. Logika Deteksi Kantuk
        if avg_ear < EAR_THRESHOLD:
            FRAME_COUNTER += 1
            
            # Jika mata tertutup cukup lama, bunyikan alarm
            if FRAME_COUNTER >= DROWSY_FRAMES_THRESHOLD:
                if not ALARM_ON:
                    ALARM_ON = True
                    # Mainkan alarm di thread terpisah agar tidak mengganggu loop utama
                    t = Thread(target=play_alarm, args=(ALARM_SOUND_PATH,))
                    t.daemon = True
                    t.start()
                
                # Tampilkan teks peringatan besar di layar
                cv2.putText(frame, "!! AWAS MENGANTUK !!", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3)
        else:
            FRAME_COUNTER = 0
            ALARM_ON = False

        # 5. Visualisasi pada Frame
        # Gambar kontur di sekitar mata
        cv2.polylines(frame, [left_eye_coords], True, (0, 255, 255), 1)
        cv2.polylines(frame, [right_eye_coords], True, (0, 255, 255), 1)
        # Tampilkan nilai EAR
        cv2.putText(frame, f"EAR: {avg_ear:.2f}", (width - 150, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        # Jika tidak ada wajah terdeteksi, reset counter
        FRAME_COUNTER = 0
        ALARM_ON = False

    # Tampilkan hasil frame ke jendela
    cv2.imshow("DrowsinessGuard", frame)
    
    # Hentikan program jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- Membersihkan ---
print("[INFO] Menutup program dan membersihkan sumber daya.")
cap.release()
cv2.destroyAllWindows()
face_mesh.close()