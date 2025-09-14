import xml.etree.ElementTree as ET

dictmanifest = {}
cnt_itemref = 0

to_remove = ['get-started',
             'integration',
             'layouts',
             'libs',
             'others',
             'overview',
             'porting',
             'widgets',
             'CONTRIBUTING.xhtml',
             'details/widgets/span.xhtml',
             'examples.xhtml',
             ]
no_linear = ['nav.xhtml',
             'index.xhtml',
             'CHANGELOG.xhtml',
             'examples.xhtml',
             'genindex.xhtml',
             'details/integration/chip/stm32.xhtml',
             ]


def manifest_fill(file_path):
    root = ET.parse(file_path).getroot()
    # Find the namespace, if present
    namespace = ''
    if '}' in root.tag:
        namespace = root.tag.split('}')[0] + '}'
    spine = root.find(f'{namespace}spine')

    if spine is None:
        print("<spine> element not found in file.")
        return

    manifest = root.find(f'{namespace}manifest')
    if manifest is None:
        print("<manifest> element not found in file.")
        return

    # Fill dictmanifest
    item = manifest.findall(f'{namespace}item')
    print("List of all <item>s inside <manifest>:")
    print('\n\n---Recreate <manifest>---\n')
    for idx, item in enumerate(item, start=1):
        id = item.get('id')
        href = item.get('href')
        dictmanifest[href] = [id, 0]
        # print(f'{dictmanifest[href][1]}    {dictmanifest[href][0]} = {href}')
    print(f'\nThere are {len(dictmanifest)} items in the manifest')


def manifest_print():
    for keys, values in dictmanifest.items():
        print(f'leggo {values[1]}    {values[0]} = {keys}')


def itemref_insert(file_path):
    global cnt_itemref

    # is_lin = any(file_path in x for x in no_linear)
    is_lin = True

    txt_is_lin = '' if is_lin else '   linear="no"'
    print(f'    <itemref idref="{dictmanifest[file_path][0]}"{txt_is_lin}/>')
    dictmanifest[file_path][1] = 99
    cnt_itemref = cnt_itemref + 1


def itemref_insert_all():
    print(f'\n\n<!--Start "spine" replacement-->\n')
    itemref_insert('nav.xhtml')   # Always present

    itemref_insert('index.xhtml')

    itemref_insert('intro/introduction/index.xhtml')
    itemref_insert('intro/introduction/requirements.xhtml')
    itemref_insert('intro/introduction/license.xhtml')
    itemref_insert('intro/introduction/faq.xhtml')
    itemref_insert('intro/introduction/repo.xhtml')

    itemref_insert('intro/getting_started/index.xhtml')
    itemref_insert('intro/getting_started/learn_the_basics.xhtml')
    itemref_insert('intro/getting_started/examples.xhtml')
    itemref_insert('intro/getting_started/whats_next.xhtml')

    # itemref_insert('examples.xhtml')

    itemref_insert('details/integration/index.xhtml')

    itemref_insert('details/integration/overview/index.xhtml')
    itemref_insert('details/integration/overview/getting_lvgl.xhtml')
    itemref_insert('details/integration/overview/building_lvgl.xhtml')
    itemref_insert('details/integration/overview/configuration.xhtml')
    itemref_insert('details/integration/overview/connecting_lvgl.xhtml')
    itemref_insert('details/integration/overview/timer_handler.xhtml')
    itemref_insert('details/integration/overview/threading.xhtml')
    itemref_insert('details/integration/overview/other_platforms.xhtml')

    itemref_insert('details/integration/pc/index.xhtml')
    itemref_insert('details/integration/pc/overview.xhtml')
    itemref_insert('details/integration/pc/linux.xhtml')
    itemref_insert('details/integration/pc/windows.xhtml')
    itemref_insert('details/integration/pc/macos.xhtml')
    itemref_insert('details/integration/pc/browser.xhtml')
    itemref_insert('details/integration/pc/sdl.xhtml')
    itemref_insert('details/integration/pc/uefi.xhtml')

    itemref_insert('details/integration/embedded_linux/index.xhtml')
    itemref_insert('details/integration/embedded_linux/overview.xhtml')

    itemref_insert('details/integration/embedded_linux/os/index.xhtml')
    itemref_insert('details/integration/embedded_linux/os/buildroot/index.xhtml')
    itemref_insert('details/integration/embedded_linux/os/buildroot/quick_setup.xhtml')
    itemref_insert('details/integration/embedded_linux/os/buildroot/image_generation.xhtml')
    itemref_insert('details/integration/embedded_linux/os/buildroot/lvgl_app.xhtml')

    itemref_insert('details/integration/embedded_linux/os/yocto/index.xhtml')
    itemref_insert('details/integration/embedded_linux/os/yocto/core_components.xhtml')
    itemref_insert('details/integration/embedded_linux/os/yocto/lvgl_recipe.xhtml')
    itemref_insert('details/integration/embedded_linux/os/yocto/terms_and_variables.xhtml')

    itemref_insert('details/integration/embedded_linux/os/torizon/torizon_os.xhtml')

    itemref_insert('details/integration/embedded_linux/drivers/index.xhtml')
    itemref_insert('details/integration/embedded_linux/drivers/fbdev.xhtml')
    itemref_insert('details/integration/embedded_linux/drivers/drm.xhtml')
    itemref_insert('details/integration/embedded_linux/drivers/opengl.xhtml')
    itemref_insert('details/integration/embedded_linux/drivers/glfw.xhtml')
    itemref_insert('details/integration/embedded_linux/drivers/egl.xhtml')
    itemref_insert('details/integration/embedded_linux/drivers/wayland.xhtml')
    itemref_insert('details/integration/embedded_linux/drivers/X11.xhtml')
    itemref_insert('details/integration/embedded_linux/drivers/evdev.xhtml')
    itemref_insert('details/integration/embedded_linux/drivers/libinput.xhtml')

    itemref_insert('details/integration/rtos/index.xhtml')
    itemref_insert('details/integration/rtos/freertos.xhtml')
    itemref_insert('details/integration/rtos/mqx.xhtml')
    itemref_insert('details/integration/rtos/nuttx.xhtml')
    itemref_insert('details/integration/rtos/px5.xhtml')
    itemref_insert('details/integration/rtos/qnx.xhtml')
    itemref_insert('details/integration/rtos/rt-thread.xhtml')
    itemref_insert('details/integration/rtos/zephyr.xhtml')

    itemref_insert('details/integration/frameworks/index.xhtml')
    itemref_insert('details/integration/frameworks/arduino.xhtml')
    itemref_insert('details/integration/frameworks/platformio.xhtml')
    itemref_insert('details/integration/frameworks/tasmota-berry.xhtml')

    itemref_insert('details/integration/boards/index.xhtml')
    itemref_insert('details/integration/boards/lvgl_supported.xhtml')
    itemref_insert('details/integration/boards/partner_supported.xhtml')

    itemref_insert('details/integration/boards/manufacturers/index.xhtml')
    itemref_insert('details/integration/boards/manufacturers/icop.xhtml')
    itemref_insert('details/integration/boards/manufacturers/toradex.xhtml')
    itemref_insert('details/integration/boards/manufacturers/riverdi.xhtml')
    itemref_insert('details/integration/boards/manufacturers/viewe.xhtml')

    itemref_insert('details/integration/chip_vendors/index.xhtml')

    itemref_insert('details/integration/chip_vendors/alif/index.xhtml')
    itemref_insert('details/integration/chip_vendors/alif/overview.xhtml')
    itemref_insert('details/integration/chip_vendors/alif/dave2d_gpu.xhtml')

    itemref_insert('details/integration/chip_vendors/arm/index.xhtml')
    itemref_insert('details/integration/chip_vendors/arm/overview.xhtml')
    itemref_insert('details/integration/chip_vendors/arm/arm2d.xhtml')

    itemref_insert('details/integration/chip_vendors/espressif/index.xhtml')
    itemref_insert('details/integration/chip_vendors/espressif/overview.xhtml')
    itemref_insert('details/integration/chip_vendors/espressif/add_lvgl_to_esp32_idf_project.xhtml')
    itemref_insert('details/integration/chip_vendors/espressif/hardware_accelerator_dma2d.xhtml')
    itemref_insert('details/integration/chip_vendors/espressif/hardware_accelerator_ppa.xhtml')
    itemref_insert('details/integration/chip_vendors/espressif/tips_and_tricks.xhtml')

    itemref_insert('details/integration/chip_vendors/nxp/index.xhtml')
    itemref_insert('details/integration/chip_vendors/nxp/overview.xhtml')
    itemref_insert('details/integration/chip_vendors/nxp/elcdif.xhtml')
    itemref_insert('details/integration/chip_vendors/nxp/pxp_gpu.xhtml')
    itemref_insert('details/integration/chip_vendors/nxp/vg_lite_gpu.xhtml')
    itemref_insert('details/integration/chip_vendors/nxp/g2d_gpu.xhtml')

    itemref_insert('details/integration/chip_vendors/renesas/index.xhtml')
    itemref_insert('details/integration/chip_vendors/renesas/built_in_drivers.xhtml')
    itemref_insert('details/integration/chip_vendors/renesas/ra_family.xhtml')
    itemref_insert('details/integration/chip_vendors/renesas/rx_family.xhtml')
    itemref_insert('details/integration/chip_vendors/renesas/rzg_family.xhtml')
    itemref_insert('details/integration/chip_vendors/renesas/rza_family.xhtml')
    itemref_insert('details/integration/chip_vendors/renesas/supported_boards.xhtml')
    itemref_insert('details/integration/chip_vendors/renesas/glcdc.xhtml')
    itemref_insert('details/integration/chip_vendors/renesas/dave2d_gpu.xhtml')

    itemref_insert('details/integration/chip_vendors/stm32/index.xhtml')
    itemref_insert('details/integration/chip_vendors/stm32/overview.xhtml')
    itemref_insert('details/integration/chip_vendors/stm32/add_lvgl_to_your_stm32_project.xhtml')
    itemref_insert('details/integration/chip_vendors/stm32/ltdc.xhtml')
    itemref_insert('details/integration/chip_vendors/stm32/neochrom.xhtml')
    itemref_insert('details/integration/chip_vendors/stm32/dma2d_gpu.xhtml')
    itemref_insert('details/integration/chip_vendors/stm32/lcd_stm32_guide.xhtml')

    itemref_insert('details/integration/external_display_controllers/index.xhtml')

    itemref_insert('details/integration/external_display_controllers/eve/index.xhtml')
    itemref_insert('details/integration/external_display_controllers/eve/frame_buffer_mode.xhtml')
    itemref_insert('details/integration/external_display_controllers/eve/gpu.xhtml')
    itemref_insert('details/integration/external_display_controllers/gen_mipi.xhtml')
    itemref_insert('details/integration/external_display_controllers/ili9341.xhtml')
    itemref_insert('details/integration/external_display_controllers/st7735.xhtml')
    itemref_insert('details/integration/external_display_controllers/st7789.xhtml')
    itemref_insert('details/integration/external_display_controllers/st7796.xhtml')

    itemref_insert('details/integration/building/index.xhtml')
    itemref_insert('details/integration/building/make.xhtml')
    itemref_insert('details/integration/building/cmake.xhtml')

    itemref_insert('details/integration/bindings/index.xhtml')
    itemref_insert('details/integration/bindings/api_json.xhtml')
    itemref_insert('details/integration/bindings/cpp.xhtml')
    itemref_insert('details/integration/bindings/javascript.xhtml')
    itemref_insert('details/integration/bindings/micropython.xhtml')
    itemref_insert('details/integration/bindings/pikascript.xhtml')

    itemref_insert('details/common-widget-features/index.xhtml')
    itemref_insert('details/common-widget-features/basics.xhtml')
    itemref_insert('details/common-widget-features/coordinates.xhtml')
    itemref_insert('details/common-widget-features/layers.xhtml')

    itemref_insert('details/common-widget-features/styles/index.xhtml')
    itemref_insert('details/common-widget-features/styles/styles.xhtml')
    itemref_insert('details/common-widget-features/styles/style-properties.xhtml')

    itemref_insert('details/common-widget-features/events.xhtml')

    itemref_insert('details/common-widget-features/layouts/index.xhtml')
    itemref_insert('details/common-widget-features/layouts/flex.xhtml')
    itemref_insert('details/common-widget-features/layouts/grid.xhtml')

    itemref_insert('details/common-widget-features/scrolling.xhtml')

    itemref_insert('details/widgets/index.xhtml')
    itemref_insert('details/widgets/base_widget.xhtml')
    itemref_insert('details/widgets/3dtexture.xhtml')
    itemref_insert('details/widgets/animimg.xhtml')
    itemref_insert('details/widgets/arc.xhtml')
    itemref_insert('details/widgets/arclabel.xhtml')
    itemref_insert('details/widgets/bar.xhtml')
    itemref_insert('details/widgets/button.xhtml')
    itemref_insert('details/widgets/buttonmatrix.xhtml')
    itemref_insert('details/widgets/calendar.xhtml')
    itemref_insert('details/widgets/canvas.xhtml')
    itemref_insert('details/widgets/chart.xhtml')
    itemref_insert('details/widgets/checkbox.xhtml')
    itemref_insert('details/widgets/dropdown.xhtml')
    itemref_insert('details/widgets/image.xhtml')
    itemref_insert('details/widgets/imagebutton.xhtml')
    itemref_insert('details/widgets/keyboard.xhtml')
    itemref_insert('details/widgets/label.xhtml')
    itemref_insert('details/widgets/led.xhtml')
    itemref_insert('details/widgets/line.xhtml')
    itemref_insert('details/widgets/list.xhtml')
    itemref_insert('details/widgets/lottie.xhtml')
    itemref_insert('details/widgets/menu.xhtml')
    itemref_insert('details/widgets/msgbox.xhtml')
    itemref_insert('details/widgets/roller.xhtml')
    itemref_insert('details/widgets/scale.xhtml')
    itemref_insert('details/widgets/slider.xhtml')
    itemref_insert('details/widgets/spangroup.xhtml')
    itemref_insert('details/widgets/spinbox.xhtml')
    itemref_insert('details/widgets/spinner.xhtml')
    itemref_insert('details/widgets/switch.xhtml')
    itemref_insert('details/widgets/table.xhtml')
    itemref_insert('details/widgets/tabview.xhtml')
    itemref_insert('details/widgets/textarea.xhtml')
    itemref_insert('details/widgets/tileview.xhtml')
    itemref_insert('details/widgets/win.xhtml')
    itemref_insert('details/widgets/new_widget.xhtml')          # Empty

    itemref_insert('details/main-modules/index.xhtml')          # Index

    itemref_insert('details/main-modules/display/index.xhtml')  # Index
    itemref_insert('details/main-modules/display/overview.xhtml')
    itemref_insert('details/main-modules/display/setup.xhtml')
    itemref_insert('details/main-modules/display/screen_layers.xhtml')
    itemref_insert('details/main-modules/display/color_format.xhtml')
    itemref_insert('details/main-modules/display/refreshing.xhtml')
    itemref_insert('details/main-modules/display/display_events.xhtml')
    itemref_insert('details/main-modules/display/resolution.xhtml')
    itemref_insert('details/main-modules/display/inactivity.xhtml')
    itemref_insert('details/main-modules/display/rotation.xhtml')
    itemref_insert('details/main-modules/display/redraw_area.xhtml')
    itemref_insert('details/main-modules/display/tiling.xhtml')
    itemref_insert('details/main-modules/display/extending_combining.xhtml')

    itemref_insert('details/main-modules/indev.xhtml')
    itemref_insert('details/main-modules/color.xhtml')
    itemref_insert('details/main-modules/font.xhtml')
    itemref_insert('details/main-modules/image.xhtml')
    itemref_insert('details/main-modules/timer.xhtml')
    itemref_insert('details/main-modules/animation.xhtml')
    itemref_insert('details/main-modules/fs.xhtml')

    itemref_insert('details/main-modules/draw/index.xhtml')
    itemref_insert('details/main-modules/draw/draw_pipeline.xhtml')
    itemref_insert('details/main-modules/draw/draw_api.xhtml')
    itemref_insert('details/main-modules/draw/draw_layers.xhtml')
    itemref_insert('details/main-modules/draw/draw_descriptors.xhtml')


    itemref_insert('details/xml/index.xhtml')

    itemref_insert('details/xml/overview/index.xhtml')
    itemref_insert('details/xml/overview/intro.xhtml')
    itemref_insert('details/xml/overview/syntax.xhtml')

    itemref_insert('details/xml/ui_elements/index.xhtml')
    itemref_insert('details/xml/ui_elements/components.xhtml')
    itemref_insert('details/xml/ui_elements/widgets.xhtml')
    itemref_insert('details/xml/ui_elements/screens.xhtml')
    itemref_insert('details/xml/ui_elements/animations.xhtml')
    itemref_insert('details/xml/ui_elements/api.xhtml')
    itemref_insert('details/xml/ui_elements/consts.xhtml')
    itemref_insert('details/xml/ui_elements/events.xhtml')
    itemref_insert('details/xml/ui_elements/preview.xhtml')
    itemref_insert('details/xml/ui_elements/styles.xhtml')
    itemref_insert('details/xml/ui_elements/view.xhtml')

    itemref_insert('details/xml/assets/index.xhtml')
    itemref_insert('details/xml/assets/images.xhtml')
    itemref_insert('details/xml/assets/fonts.xhtml')

    itemref_insert('details/xml/features/index.xhtml')
    itemref_insert('details/xml/features/subjects.xhtml')
    itemref_insert('details/xml/features/tests.xhtml')
    itemref_insert('details/xml/features/translations.xhtml')

    itemref_insert('details/xml/license.xhtml')


    itemref_insert('details/auxiliary-modules/index.xhtml')

    itemref_insert('details/auxiliary-modules/file_explorer.xhtml')
    itemref_insert('details/auxiliary-modules/font_manager.xhtml')
    itemref_insert('details/auxiliary-modules/fragment.xhtml')
    itemref_insert('details/auxiliary-modules/gridnav.xhtml')
    itemref_insert('details/auxiliary-modules/ime_pinyin.xhtml')
    itemref_insert('details/auxiliary-modules/imgfont.xhtml')
    itemref_insert('details/auxiliary-modules/monkey.xhtml')
    itemref_insert('details/auxiliary-modules/obj_id.xhtml')
    itemref_insert('details/auxiliary-modules/obj_property.xhtml')

    itemref_insert('details/auxiliary-modules/observer/index.xhtml')
    itemref_insert('details/auxiliary-modules/observer/observer.xhtml')
    itemref_insert('details/auxiliary-modules/observer/observer_examples.xhtml')

    itemref_insert('details/auxiliary-modules/snapshot.xhtml')
    itemref_insert('details/auxiliary-modules/sysmon.xhtml')
    itemref_insert('details/auxiliary-modules/test.xhtml')
    itemref_insert('details/auxiliary-modules/translation.xhtml')

    itemref_insert('details/libs/index.xhtml')
    itemref_insert('details/libs/arduino_esp_littlefs.xhtml')
    itemref_insert('details/libs/arduino_sd.xhtml')
    itemref_insert('details/libs/barcode.xhtml')
    itemref_insert('details/libs/bmp.xhtml')
    itemref_insert('details/libs/ffmpeg.xhtml')
    itemref_insert('details/libs/freetype.xhtml')
    itemref_insert('details/libs/fs.xhtml')
    itemref_insert('details/libs/gif.xhtml')
    itemref_insert('details/libs/gstreamer.xhtml')
    itemref_insert('details/libs/gltf.xhtml')
    itemref_insert('details/libs/lfs.xhtml')
    itemref_insert('details/libs/libjpeg_turbo.xhtml')
    itemref_insert('details/libs/libpng.xhtml')
    itemref_insert('details/libs/lodepng.xhtml')
    itemref_insert('details/libs/qrcode.xhtml')
    itemref_insert('details/libs/rle.xhtml')
    itemref_insert('details/libs/rlottie.xhtml')
    itemref_insert('details/libs/svg.xhtml')
    itemref_insert('details/libs/tiny_ttf.xhtml')
    itemref_insert('details/libs/tjpgd.xhtml')

    itemref_insert('details/debugging/index.xhtml')
    itemref_insert('details/debugging/gdb_plugin.xhtml')
    itemref_insert('details/debugging/log.xhtml')
    itemref_insert('details/debugging/profiler.xhtml')
    itemref_insert('details/debugging/vg_lite_tvg.xhtml')

    itemref_insert('contributing/index.xhtml')
    itemref_insert('contributing/introduction.xhtml')
    itemref_insert('contributing/ways_to_contribute.xhtml')
    itemref_insert('contributing/pull_requests.xhtml')
    itemref_insert('contributing/dco.xhtml')
    itemref_insert('contributing/coding_style.xhtml')

    itemref_insert('CHANGELOG.xhtml')


def manifest_print_remaining():
    print(f'\n\n<!--UNSORTED-->\n\n\n')
    n_handled = 0
    n_unhandled = 0
    for keys, values in dictmanifest.items():
        if values[1] == 0:
            if any(keys.startswith(prefix) for prefix in to_remove):
                pass
            else:
                n_unhandled = n_unhandled+1
                # print(f'    <itemref idref="{values[0]}"   linear="no"/>     <!--{keys}--> ')
                print(f'    <itemref idref="{values[0]}"/>     <!--{keys}--> ')
        else:
            n_handled = n_handled+1
    # print(f'\n\n {n_handled} handled, {n_unhandled} NOT handled total={n_handled+n_unhandled}/{len(dictmanifest)}')


def list_removed():
    print(f'\n\n<!--TO REMOVE-->\n\n\n')
    for keys, values in dictmanifest.items():
        # if  any(file_path in x for x in my_list)
        if any(keys.startswith(prefix) for prefix in to_remove):
            print(f'    <itemref idref="{values[0]}"/>     <!--{keys} (to remove)--> ')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    manifest_fill('content.opf')

    itemref_insert_all()

    # manifest_print()
    manifest_print_remaining()
    list_removed()
    print(f'\n\n<!--END "spine" replacement-->\n')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
