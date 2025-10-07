#include "opencv2/objdetect.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include <iostream>

using namespace std;
using namespace cv;

int main()
{
    // Загрузка изображения
    Mat image = imread("test_face.jpg");
    if (image.empty()) {
        cout << "Could not open image!" << endl;
        return -1;
    }

    // Загрузка каскада для распознавания лиц
    CascadeClassifier face_cascade;
    if (!face_cascade.load("haarcascade_frontalface_alt2.xml")) {
        cout << "Error loading cascade file!" << endl;
        return -1;
    }

    // Обнаружение лиц
    vector<Rect> faces;
    face_cascade.detectMultiScale(image, faces, 1.1, 3, 0, Size(30, 30));

    // Рисование прямоугольников вокруг лиц
    for (size_t i = 0; i < faces.size(); i++) {
        rectangle(image, faces[i], Scalar(255, 0, 0), 2);
    }

    // Сохранение результата
    imwrite("result.jpg", image);
    cout << "Found " << faces.size() << " faces. Result saved to result.jpg" << endl;

    return 0;
}