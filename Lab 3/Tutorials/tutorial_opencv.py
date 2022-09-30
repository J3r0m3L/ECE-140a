import cv2

# Question 1
def first_question():
    img1 = cv2.imread("./Tutorial_Pyramid_Basics/public/geisel.jpg")
    img1[:, :, 0] = 255 - img1[:, :, 0]
    cv2.imshow("Inverted Blue Colorspace Image", img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Question 2
def second_question():
    img2 = cv2.imread("./Tutorial_Pyramid_Basics/public/geisel.jpg")
    image_dimensions = img2[:, :, 0].shape    
    img2 = cv2.resize(img2, image_dimensions)
    cv2.imshow("Squished Image", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def main():
    #first_question()
    second_question()

if __name__ == "__main__":
    main()