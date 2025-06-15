# Game loop utama
while running:
    dt = clock.tick(60)
    animation_timer += dt

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                holding_tool = True
                current_item = get_current_selected_item()
                print(f"Karakter sekarang memegang {current_item}.")
            elif event.key == pygame.K_q:
                holding_tool = False
                using_tool = False
                print("Karakter melepas alat.")
            elif event.key == pygame.K_SPACE and holding_tool:
                using_tool = True
            elif event.key == pygame.K_f:
                if not inside_house and check_house_collision(x, y):
                    inside_house = True
                    x, y = 100.0, 200.0  # Posisi spawn dalam rumah
                    print("Masuk ke dalam rumah")
                elif inside_house:
                    inside_house = False
                    x, y = house_x + 100, house_y + 170  # Posisi keluar rumah
                    print("Keluar dari rumah")
            elif event.key == pygame.K_RETURN:
                # Panen buah satu per satu dari pohon terdekat
                harvested = False
                for tree in trees:
                    if tree.is_near((x, y)) and tree.has_available_fruits():
                        if tree.harvest_single_fruit((x, y)):
                            add_to_inventory("buah")
                            fruit_count = count_item_in_inventory("buah")
                            print(f"Satu buah dipanen! Total buah: {fruit_count}")
                            harvested = True
                            break
                if not harvested:
                    print("Tidak ada buah yang bisa dipanen di sekitar sini.")
            elif event.key == pygame.K_RIGHT:
                # Ganti ke item berikutnya di inventory
                unique_items = {}
                for item in inventory:
                    unique_items[item] = unique_items.get(item, 0) + 1
                if unique_items:
                    selected_index = (selected_index + 1) % len(unique_items)
                    print(f"Item dipilih: {get_current_selected_item()}")
            elif event.key == pygame.K_LEFT:
                # Ganti ke item sebelumnya di inventory
                unique_items = {}
                for item in inventory:
                    unique_items[item] = unique_items.get(item, 0) + 1
                if unique_items:
                    selected_index = (selected_index - 1) % len(unique_items)
                    print(f"Item dipilih: {get_current_selected_item()}")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                using_tool = False

    # Input gerakan
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    moved = False

    if keys[pygame.K_w]:
        dy = -1
        direction = "up"
        moved = True
    elif keys[pygame.K_s]:
        dy = 1
        direction = "down"
        moved = True
    elif keys[pygame.K_a]:
        dx = -1
        direction = "left"
        moved = True
    elif keys[pygame.K_d]:
        dx = 1
        direction = "right"
        moved = True

    # Update posisi karakter dengan collision detection yang diperbaiki
    new_x = x + dx * speed * dt
    new_y = y + dy * speed * dt
