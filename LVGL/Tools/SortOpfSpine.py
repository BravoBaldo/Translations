import xml.etree.ElementTree as ET
import winsound

dictmanifest = {}
cnt_itemref = 0

to_remove = ['get-started', #
             'integration/framework/', #
             'integration/ide/', #
             'integration/os/', #
             'layouts',     #
#             'libs',
             'details',      #
             'others',      #
             'overview',    #
             'porting',     #
#             'widgets',
             'CONTRIBUTING.xhtml',
             'widgets/span.xhtml',
#             'examples.xhtml',
             'intro/get-started/index.xhtml',
#             'getting_started/index.xhtml',
             'intro/getting_started/index.xhtml',
             'widgets/obj.xhtml',
             ]
no_linear = ['nav.xhtml',
             'index.xhtml',
             'CHANGELOG.xhtml',
             'examples.xhtml',
             'genindex.xhtml',
             'integration/chip/stm32.xhtml',
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
        i = item.get('id')
        href = item.get('href')
        dictmanifest[href] = [i, 0]
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


    # introduction
    itemref_insert('introduction/index.xhtml')
    itemref_insert('introduction/requirements.xhtml')
    itemref_insert('introduction/license.xhtml')
    itemref_insert('introduction/faq.xhtml')
    itemref_insert('introduction/repo.xhtml')

    # getting_started
    itemref_insert('getting_started/index.xhtml')
    itemref_insert('getting_started/learn_the_basics.xhtml')
    itemref_insert('getting_started/examples.xhtml')
    itemref_insert('getting_started/whats_next.xhtml')

    # examples
    # itemref_insert('examples.xhtml')

    # integration
    itemref_insert('integration/index.xhtml')

    itemref_insert('integration/overview/index.xhtml')
    itemref_insert('integration/overview/getting_lvgl.xhtml')
    itemref_insert('integration/overview/building_lvgl.xhtml')
    itemref_insert('integration/overview/configuration.xhtml')
    itemref_insert('integration/overview/connecting_lvgl.xhtml')
    itemref_insert('integration/overview/timer_handler.xhtml')
    itemref_insert('integration/overview/threading.xhtml')
    itemref_insert('integration/overview/other_platforms.xhtml')

    itemref_insert('integration/pc/index.xhtml')
    itemref_insert('integration/pc/linux.xhtml')
    itemref_insert('integration/pc/windows.xhtml')
    itemref_insert('integration/pc/macos.xhtml')
    itemref_insert('integration/pc/browser.xhtml')
    itemref_insert('integration/pc/sdl.xhtml')
    itemref_insert('integration/pc/uefi.xhtml')

    itemref_insert('integration/embedded_linux/index.xhtml')
    itemref_insert('integration/embedded_linux/overview.xhtml')
    itemref_insert('integration/embedded_linux/opengl.xhtml')

    itemref_insert('integration/embedded_linux/os/index.xhtml')
    itemref_insert('integration/embedded_linux/os/buildroot/index.xhtml')
    itemref_insert('integration/embedded_linux/os/buildroot/quick_setup.xhtml')
    itemref_insert('integration/embedded_linux/os/buildroot/image_generation.xhtml')
    itemref_insert('integration/embedded_linux/os/buildroot/lvgl_app.xhtml')

    itemref_insert('integration/embedded_linux/os/yocto/index.xhtml')
    itemref_insert('integration/embedded_linux/os/yocto/core_components.xhtml')
    itemref_insert('integration/embedded_linux/os/yocto/lvgl_recipe.xhtml')
    itemref_insert('integration/embedded_linux/os/yocto/terms_and_variables.xhtml')

    itemref_insert('integration/embedded_linux/os/torizon/torizon_os.xhtml')

    itemref_insert('integration/embedded_linux/drivers/index.xhtml')
    itemref_insert('integration/embedded_linux/drivers/fbdev.xhtml')
    itemref_insert('integration/embedded_linux/drivers/drm.xhtml')
    itemref_insert('integration/embedded_linux/drivers/opengl_driver.xhtml')
    itemref_insert('integration/embedded_linux/drivers/glfw.xhtml')
    itemref_insert('integration/embedded_linux/drivers/egl.xhtml')
    itemref_insert('integration/embedded_linux/drivers/wayland.xhtml')
    itemref_insert('integration/embedded_linux/drivers/X11.xhtml')
    itemref_insert('integration/embedded_linux/drivers/evdev.xhtml')
    itemref_insert('integration/embedded_linux/drivers/libinput.xhtml')

    itemref_insert('integration/rtos/index.xhtml')
    itemref_insert('integration/rtos/freertos.xhtml')
    itemref_insert('integration/rtos/mqx.xhtml')
    itemref_insert('integration/rtos/nuttx.xhtml')
    itemref_insert('integration/rtos/px5.xhtml')
    itemref_insert('integration/rtos/qnx.xhtml')
    itemref_insert('integration/rtos/rt-thread.xhtml')
    itemref_insert('integration/rtos/zephyr.xhtml')

    itemref_insert('integration/frameworks/index.xhtml')
    itemref_insert('integration/frameworks/arduino.xhtml')
    itemref_insert('integration/frameworks/platformio.xhtml')
    itemref_insert('integration/frameworks/tasmota-berry.xhtml')

    itemref_insert('integration/boards/index.xhtml')
    itemref_insert('integration/boards/lvgl_supported.xhtml')
    itemref_insert('integration/boards/partner_supported.xhtml')

    itemref_insert('integration/boards/manufacturers/index.xhtml')
    itemref_insert('integration/boards/manufacturers/icop.xhtml')
    itemref_insert('integration/boards/manufacturers/toradex.xhtml')
    itemref_insert('integration/boards/manufacturers/riverdi.xhtml')
    itemref_insert('integration/boards/manufacturers/viewe.xhtml')

    itemref_insert('integration/chip_vendors/index.xhtml')

    itemref_insert('integration/chip_vendors/alif/index.xhtml')
    itemref_insert('integration/chip_vendors/alif/overview.xhtml')
    itemref_insert('integration/chip_vendors/alif/dave2d_gpu.xhtml')

    itemref_insert('integration/chip_vendors/arm/index.xhtml')
    itemref_insert('integration/chip_vendors/arm/overview.xhtml')
    itemref_insert('integration/chip_vendors/arm/arm2d.xhtml')

    itemref_insert('integration/chip_vendors/espressif/index.xhtml')
    itemref_insert('integration/chip_vendors/espressif/overview.xhtml')
    itemref_insert('integration/chip_vendors/espressif/add_lvgl_to_esp32_idf_project.xhtml')
    itemref_insert('integration/chip_vendors/espressif/hardware_accelerator_dma2d.xhtml')
    itemref_insert('integration/chip_vendors/espressif/hardware_accelerator_ppa.xhtml')
    itemref_insert('integration/chip_vendors/espressif/tips_and_tricks.xhtml')

    itemref_insert('integration/chip_vendors/nxp/index.xhtml')
    itemref_insert('integration/chip_vendors/nxp/overview.xhtml')
    itemref_insert('integration/chip_vendors/nxp/elcdif.xhtml')
    itemref_insert('integration/chip_vendors/nxp/pxp_gpu.xhtml')
    itemref_insert('integration/chip_vendors/nxp/vg_lite_gpu.xhtml')
    itemref_insert('integration/chip_vendors/nxp/g2d_gpu.xhtml')

    itemref_insert('integration/chip_vendors/renesas/index.xhtml')
    itemref_insert('integration/chip_vendors/renesas/built_in_drivers.xhtml')
    itemref_insert('integration/chip_vendors/renesas/ra_family.xhtml')
    itemref_insert('integration/chip_vendors/renesas/rx_family.xhtml')
    itemref_insert('integration/chip_vendors/renesas/rzg_family.xhtml')
    itemref_insert('integration/chip_vendors/renesas/rza_family.xhtml')
    itemref_insert('integration/chip_vendors/renesas/supported_boards.xhtml')
    itemref_insert('integration/chip_vendors/renesas/glcdc.xhtml')
    itemref_insert('integration/chip_vendors/renesas/dave2d_gpu.xhtml')

    itemref_insert('integration/chip_vendors/stm32/index.xhtml')
    itemref_insert('integration/chip_vendors/stm32/overview.xhtml')
    itemref_insert('integration/chip_vendors/stm32/add_lvgl_to_your_stm32_project.xhtml')
    itemref_insert('integration/chip_vendors/stm32/ltdc.xhtml')
    itemref_insert('integration/chip_vendors/stm32/neochrom.xhtml')
    itemref_insert('integration/chip_vendors/stm32/dma2d_gpu.xhtml')
    itemref_insert('integration/chip_vendors/stm32/lcd_stm32_guide.xhtml')

    itemref_insert('integration/external_display_controllers/index.xhtml')

    itemref_insert('integration/external_display_controllers/eve/index.xhtml')
    itemref_insert('integration/external_display_controllers/eve/frame_buffer_mode.xhtml')
    itemref_insert('integration/external_display_controllers/eve/gpu.xhtml')
    itemref_insert('integration/external_display_controllers/gen_mipi.xhtml')
    itemref_insert('integration/external_display_controllers/ili9341.xhtml')
    itemref_insert('integration/external_display_controllers/st7735.xhtml')
    itemref_insert('integration/external_display_controllers/st7789.xhtml')
    itemref_insert('integration/external_display_controllers/st7796.xhtml')
    itemref_insert('integration/external_display_controllers/nv3007.xhtml')

    itemref_insert('integration/building/index.xhtml')
    itemref_insert('integration/building/make.xhtml')
    itemref_insert('integration/building/cmake.xhtml')

    itemref_insert('integration/bindings/index.xhtml')
    itemref_insert('integration/bindings/api_json.xhtml')
    itemref_insert('integration/bindings/cpp.xhtml')
    itemref_insert('integration/bindings/javascript.xhtml')
    itemref_insert('integration/bindings/micropython.xhtml')
    itemref_insert('integration/bindings/pikascript.xhtml')

    #common-widget-features
    itemref_insert('common-widget-features/index.xhtml')
    itemref_insert('common-widget-features/basics.xhtml')
    itemref_insert('common-widget-features/api.xhtml')
    itemref_insert('common-widget-features/tree.xhtml')
    itemref_insert('common-widget-features/screens.xhtml')
    itemref_insert('common-widget-features/coordinates.xhtml')
    itemref_insert('common-widget-features/parts_and_states.xhtml')

    itemref_insert('common-widget-features/layers.xhtml')

    itemref_insert('common-widget-features/styles/index.xhtml')
    itemref_insert('common-widget-features/styles/overview.xhtml')
    itemref_insert('common-widget-features/styles/style_sheets.xhtml')
    itemref_insert('common-widget-features/styles/local_styles.xhtml')
    itemref_insert('common-widget-features/styles/transitions.xhtml')
    itemref_insert('common-widget-features/styles/themes.xhtml')
    itemref_insert('common-widget-features/styles/style-properties.xhtml')

    itemref_insert('common-widget-features/events.xhtml')
    itemref_insert('common-widget-features/flags.xhtml')

    itemref_insert('common-widget-features/layouts/index.xhtml')
    itemref_insert('common-widget-features/layouts/overview.xhtml')
    itemref_insert('common-widget-features/layouts/flex.xhtml')
    itemref_insert('common-widget-features/layouts/grid.xhtml')

    itemref_insert('common-widget-features/scrolling.xhtml')

    # widgets
    itemref_insert('widgets/index.xhtml')
    itemref_insert('widgets/base_widget.xhtml')
    itemref_insert('widgets/3dtexture.xhtml')
    itemref_insert('widgets/animimg.xhtml')
    itemref_insert('widgets/arc.xhtml')
    itemref_insert('widgets/arclabel.xhtml')
    itemref_insert('widgets/bar.xhtml')
    itemref_insert('widgets/button.xhtml')
    itemref_insert('widgets/buttonmatrix.xhtml')
    itemref_insert('widgets/calendar.xhtml')
    itemref_insert('widgets/canvas.xhtml')
    itemref_insert('widgets/chart.xhtml')
    itemref_insert('widgets/checkbox.xhtml')
    itemref_insert('widgets/dropdown.xhtml')
    itemref_insert('widgets/image.xhtml')
    itemref_insert('widgets/imagebutton.xhtml')
    itemref_insert('widgets/ime_pinyin.xhtml')
    itemref_insert('widgets/keyboard.xhtml')
    itemref_insert('widgets/label.xhtml')
    itemref_insert('widgets/led.xhtml')
    itemref_insert('widgets/line.xhtml')
    itemref_insert('widgets/list.xhtml')
    itemref_insert('widgets/lottie.xhtml')
    itemref_insert('widgets/menu.xhtml')
    itemref_insert('widgets/msgbox.xhtml')
    itemref_insert('widgets/roller.xhtml')
    itemref_insert('widgets/scale.xhtml')
    itemref_insert('widgets/slider.xhtml')
    itemref_insert('widgets/spangroup.xhtml')
    itemref_insert('widgets/spinbox.xhtml')
    itemref_insert('widgets/spinner.xhtml')
    itemref_insert('widgets/switch.xhtml')
    itemref_insert('widgets/table.xhtml')
    itemref_insert('widgets/tabview.xhtml')
    itemref_insert('widgets/textarea.xhtml')
    itemref_insert('widgets/tileview.xhtml')
    itemref_insert('widgets/win.xhtml')
    itemref_insert('widgets/new_widget.xhtml')          # Empty

    # main-modules
    itemref_insert('main-modules/index.xhtml')          # Index

    itemref_insert('main-modules/display/index.xhtml')  # Index
    itemref_insert('main-modules/display/overview.xhtml')
    itemref_insert('main-modules/display/setup.xhtml')
    itemref_insert('main-modules/display/screen_layers.xhtml')
    itemref_insert('main-modules/display/color_format.xhtml')
    itemref_insert('main-modules/display/refreshing.xhtml')
    itemref_insert('main-modules/display/display_events.xhtml')
    itemref_insert('main-modules/display/resolution.xhtml')
    itemref_insert('main-modules/display/inactivity.xhtml')
    itemref_insert('main-modules/display/rotation.xhtml')
    itemref_insert('main-modules/display/redraw_area.xhtml')
    itemref_insert('main-modules/display/tiling.xhtml')
    itemref_insert('main-modules/display/extending_combining.xhtml')

    itemref_insert('main-modules/indev/index.xhtml')
    itemref_insert('main-modules/indev/overview.xhtml')
    itemref_insert('main-modules/indev/pointer.xhtml')
    itemref_insert('main-modules/indev/keypad.xhtml')
    itemref_insert('main-modules/indev/encoder.xhtml')
    itemref_insert('main-modules/indev/button.xhtml')
    itemref_insert('main-modules/indev/groups.xhtml')
    itemref_insert('main-modules/indev/gestures.xhtml')
    itemref_insert('main-modules/indev/gridnav.xhtml')

    itemref_insert('main-modules/fonts/index.xhtml')
    itemref_insert('main-modules/fonts/overview.xhtml')
    itemref_insert('main-modules/fonts/built_in_fonts.xhtml')
    itemref_insert('main-modules/fonts/binfont_loader.xhtml')
    itemref_insert('main-modules/fonts/imgfont.xhtml')
    itemref_insert('main-modules/fonts/bdf_fonts.xhtml')
    itemref_insert('main-modules/fonts/rtl.xhtml')
    itemref_insert('main-modules/fonts/new_font_engine.xhtml')
    itemref_insert('main-modules/fonts/font_manager.xhtml')

    itemref_insert('main-modules/color.xhtml')
    itemref_insert('main-modules/timer.xhtml')
    itemref_insert('main-modules/animation.xhtml')
    itemref_insert('main-modules/fs.xhtml')

    itemref_insert('main-modules/observer/index.xhtml')
    itemref_insert('main-modules/observer/observer.xhtml')
    itemref_insert('main-modules/observer/observer_examples.xhtml')

    itemref_insert('main-modules/draw/index.xhtml')
    itemref_insert('main-modules/draw/draw_pipeline.xhtml')
    itemref_insert('main-modules/draw/draw_api.xhtml')
    itemref_insert('main-modules/draw/draw_layers.xhtml')
    itemref_insert('main-modules/draw/draw_descriptors.xhtml')
    itemref_insert('main-modules/draw/snapshot.xhtml')

    # xml
    itemref_insert('xml/index.xhtml')
    itemref_insert('xml/intro.xhtml')
    itemref_insert('xml/learn_by_examples.xhtml')

    itemref_insert('xml/editor/index.xhtml')
    itemref_insert('xml/editor/overview.xhtml')
    itemref_insert('xml/editor/install.xhtml')
    itemref_insert('xml/editor/user_interface.xhtml')
    itemref_insert('xml/editor/hotkeys.xhtml')
    itemref_insert('xml/editor/license.xhtml')

    itemref_insert('xml/xml/index.xhtml')
    itemref_insert('xml/xml/overview.xhtml')
    itemref_insert('xml/xml/syntax.xhtml')
    itemref_insert('xml/xml/license.xhtml')

    itemref_insert('xml/integration/index.xhtml')
    itemref_insert('xml/integration/c_code.xhtml')
    itemref_insert('xml/integration/xml.xhtml')
    itemref_insert('xml/integration/renesas-dev-tools.xhtml')
    itemref_insert('xml/integration/arduino.xhtml')

    itemref_insert('xml/ui_elements/index.xhtml')
    itemref_insert('xml/ui_elements/components.xhtml')
    itemref_insert('xml/ui_elements/widgets.xhtml')
    itemref_insert('xml/ui_elements/screens.xhtml')
    itemref_insert('xml/ui_elements/animations.xhtml')
    itemref_insert('xml/ui_elements/api.xhtml')
    itemref_insert('xml/ui_elements/consts.xhtml')
    itemref_insert('xml/ui_elements/events.xhtml')
    itemref_insert('xml/ui_elements/preview.xhtml')
    itemref_insert('xml/ui_elements/styles.xhtml')
    itemref_insert('xml/ui_elements/view.xhtml')

    itemref_insert('xml/assets/index.xhtml')
    itemref_insert('xml/assets/images.xhtml')
    itemref_insert('xml/assets/fonts.xhtml')

    itemref_insert('xml/features/index.xhtml')
    itemref_insert('xml/features/subjects.xhtml')
    itemref_insert('xml/features/tests.xhtml')
    itemref_insert('xml/features/translations.xhtml')

    itemref_insert('xml/tools/index.xhtml')
    itemref_insert('xml/tools/cli.xhtml')
    itemref_insert('xml/tools/online_share.xhtml')
    itemref_insert('xml/tools/figma.xhtml')

    # auxiliary-modules
    itemref_insert('auxiliary-modules/index.xhtml')
    itemref_insert('auxiliary-modules/file_explorer.xhtml')
    itemref_insert('auxiliary-modules/fragment.xhtml')
    itemref_insert('auxiliary-modules/obj_property.xhtml')
    itemref_insert('auxiliary-modules/translation.xhtml')

    # libs
    itemref_insert('libs/index.xhtml')

    itemref_insert('libs/font_support/index.xhtml')
    itemref_insert('libs/font_support/freetype.xhtml')
    itemref_insert('libs/font_support/tiny_ttf.xhtml')

    itemref_insert('libs/fs_support/index.xhtml')
    itemref_insert('libs/fs_support/fs.xhtml')
    itemref_insert('libs/fs_support/arduino_esp_littlefs.xhtml')
    itemref_insert('libs/fs_support/arduino_sd.xhtml')
    itemref_insert('libs/fs_support/frogfs.xhtml')
    itemref_insert('libs/fs_support/lfs.xhtml')

    itemref_insert('libs/image_support/index.xhtml')
    itemref_insert('libs/image_support/bmp.xhtml')
    itemref_insert('libs/image_support/gif.xhtml')
    itemref_insert('libs/image_support/libjpeg_turbo.xhtml')
    itemref_insert('libs/image_support/libpng.xhtml')
    itemref_insert('libs/image_support/lodepng.xhtml')
    itemref_insert('libs/image_support/libwebp.xhtml')
    itemref_insert('libs/image_support/lz4.xhtml')
    itemref_insert('libs/image_support/rle.xhtml')
    itemref_insert('libs/image_support/rlottie.xhtml')
    itemref_insert('libs/image_support/svg.xhtml')
    itemref_insert('libs/image_support/tjpgd.xhtml')

    itemref_insert('libs/video_support/index.xhtml')
    itemref_insert('libs/video_support/ffmpeg.xhtml')
    itemref_insert('libs/video_support/gstreamer.xhtml')

    itemref_insert('libs/barcode.xhtml')
    itemref_insert('libs/gltf.xhtml')
    itemref_insert('libs/qrcode.xhtml')

    # debugging
    itemref_insert('debugging/index.xhtml')
    itemref_insert('debugging/gdb_plugin.xhtml')
    itemref_insert('debugging/log.xhtml')

    itemref_insert('debugging/monkey.xhtml')
    itemref_insert('debugging/obj_id.xhtml')
    itemref_insert('debugging/monkey.xhtml')
    itemref_insert('debugging/profiler.xhtml')
    itemref_insert('debugging/sysmon.xhtml')
    itemref_insert('debugging/test.xhtml')
    itemref_insert('debugging/vg_lite_tvg.xhtml')

    # guides

    # contributing
    itemref_insert('contributing/index.xhtml')
    itemref_insert('contributing/introduction.xhtml')
    itemref_insert('contributing/ways_to_contribute.xhtml')
    itemref_insert('contributing/pull_requests.xhtml')
    itemref_insert('contributing/dco.xhtml')
    itemref_insert('contributing/coding_style.xhtml')

    # CHANGELOG
    itemref_insert('CHANGELOG.xhtml')

    # API
    itemref_insert('API/lv_api_map_v8_h.xhtml')
    itemref_insert('API/lv_api_map_v9_0_h.xhtml')
    itemref_insert('API/lv_api_map_v9_1_h.xhtml')
    itemref_insert('API/lv_api_map_v9_2_h.xhtml')
    itemref_insert('API/lv_api_map_v9_3_h.xhtml')
    itemref_insert('API/lv_api_map_v9_4_h.xhtml')
    itemref_insert('API/lv_conf_internal_h.xhtml')
    itemref_insert('API/lv_conf_kconfig_h.xhtml')
    itemref_insert('API/lv_init_h.xhtml')
    itemref_insert('API/lvgl_h.xhtml')
    itemref_insert('API/lvgl_private_h.xhtml')
    itemref_insert('API/core/index.xhtml')
    itemref_insert('API/debugging/index.xhtml')
    itemref_insert('API/display/index.xhtml')
    itemref_insert('API/draw/index.xhtml')
    itemref_insert('API/drivers/index.xhtml')
    itemref_insert('API/font/index.xhtml')
    itemref_insert('API/indev/index.xhtml')
    itemref_insert('API/layouts/index.xhtml')
    itemref_insert('API/libs/index.xhtml')
    itemref_insert('API/misc/index.xhtml')
    itemref_insert('API/osal/index.xhtml')
    itemref_insert('API/others/index.xhtml')
    itemref_insert('API/stdlib/index.xhtml')
    itemref_insert('API/themes/index.xhtml')
    itemref_insert('API/tick/index.xhtml')
    itemref_insert('API/widgets/index.xhtml')
    itemref_insert('API/xml/index.xhtml')


def manifest_print_remaining():
    print(f'\n\n<!--UNSORTED-->\n\n\n')
    n_handled = 0
    n_unhandled = 0
    for keys, values in dictmanifest.items():
        if values[1] == 0:
            if any(keys.startswith(prefix) for prefix in to_remove):
                pass
            else:
                suspect = ""  #  "\tSUSPECT TO ADD" if keys.startswith("details/") else ""
                if suspect != "":
                    winsound.Beep(2000, 100)
                n_unhandled = n_unhandled+1
                print(f'    <itemref idref="{values[0]}"/>     <!--{keys}   {suspect}--> ')
        else:
            n_handled = n_handled+1


def list_removed():
    print(f'\n\n<!--TO REMOVE-->\n\n\n')
    for keys, values in dictmanifest.items():
        # if  any(file_path in x for x in my_list)
        if any(keys.startswith(prefix) for prefix in to_remove):
            print(f'    <itemref idref="{values[0]}"/>     <!--{keys} (to remove)--> ')


if __name__ == '__main__':
    manifest_fill('../LVGL_Italiano/epub/it/content.opf')
    # manifest_fill('content.opf')

    itemref_insert_all()

    # manifest_print()
    manifest_print_remaining()
    list_removed()
    print(f'\n\n<!--END "spine" replacement-->\n')

