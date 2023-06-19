import cv2

cap = cv2.VideoCapture('C:/Users/syu/Videos/2022_08_20_09_38_52.mkv')
total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(total_frame)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        # You can perform various operations on the frames here
        cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()