struct Image {
	int width;
	int height;
	char *data;
}

struct Image Image;
Image.width = 100;
Image.height = 100;
Image.data = malloc(sizeof(char) * Image.width * Image.height)