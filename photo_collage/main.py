from square_cropper.color import save_top4_color_grid

def main():
    input_path: str = "./square_cropper/testing_image.jpeg"
    color_grid_path = save_top4_color_grid(input_path, size=256)
    print(f"Saved top-4 color grid to: {color_grid_path}")

if __name__ == "__main__":
    main()
