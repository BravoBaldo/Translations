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

    # integration
    itemref_insert('integration/index.xhtml')
    itemref_insert('integration/overview.xhtml')

    itemref_insert('integration/pc/index.xhtml')
    itemref_insert('integration/pc/linux.xhtml')
    itemref_insert('integration/pc/windows.xhtml')
    itemref_insert('integration/pc/macos.xhtml')
    itemref_insert('integration/pc/browser.xhtml')
    itemref_insert('integration/pc/sdl.xhtml')
    itemref_insert('integration/pc/uefi.xhtml')

    itemref_insert('integration/embedded_linux/index.xhtml')
    itemref_insert('integration/embedded_linux/opengl.xhtml')
    itemref_insert('integration/embedded_linux/draw_opengl.xhtml')
    itemref_insert('integration/embedded_linux/draw_sdl.xhtml')
    itemref_insert('integration/embedded_linux/nanovg.xhtml')

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
    itemref_insert('common-widget-features/obj_property.xhtml')

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

    itemref_insert('main-modules/images/index.xhtml')
    itemref_insert('main-modules/images/overview.xhtml')
    itemref_insert('main-modules/images/sources.xhtml')
    itemref_insert('main-modules/images/color_formats.xhtml')
    itemref_insert('main-modules/images/adding_images.xhtml')
    itemref_insert('main-modules/images/using_images.xhtml')
    itemref_insert('main-modules/images/decoders.xhtml')
    itemref_insert('main-modules/images/caching.xhtml')

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

    itemref_insert('main-modules/translation.xhtml')

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
    itemref_insert('xml/integration/zephyr.xhtml')

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
    #itemref_insert('auxiliary-modules/obj_property.xhtml')
    #itemref_insert('auxiliary-modules/translation.xhtml')

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
    # itemref_insert('libs/image_support/gif.xhtml')
    itemref_insert('widgets/gif.xhtml')

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
    itemref_insert('guides/index.xhtml')
    itemref_insert('guides/how-to-articles/index.xhtml')
    itemref_insert('guides/internal-subsystems/index.xhtml')

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
    itemref_insert('API/index.xhtml')

    itemref_insert('API/lv_api_map_v8_h.xhtml')
    itemref_insert('API/lv_api_map_v9_0_h.xhtml')
    itemref_insert('API/lv_api_map_v9_1_h.xhtml')
    itemref_insert('API/lv_api_map_v9_2_h.xhtml')
    itemref_insert('API/lv_api_map_v9_3_h.xhtml')
    itemref_insert('API/lv_api_map_v9_4_h.xhtml')
    itemref_insert('API/lv_conf_h.xhtml')
    itemref_insert('API/lv_conf_kconfig_h.xhtml')
    itemref_insert('API/lv_init_h.xhtml')
    itemref_insert('API/lvgl_h.xhtml')
    itemref_insert('API/lvgl_private_h.xhtml')

    itemref_insert('API/core/index.xhtml')
    itemref_insert('API/core/index.xhtml')
    itemref_insert('API/core/lv_global_h.xhtml')
    itemref_insert('API/core/lv_group_h.xhtml')
    itemref_insert('API/core/lv_group_private_h.xhtml')
    itemref_insert('API/core/lv_obj_h.xhtml')
    itemref_insert('API/core/lv_obj_class_h.xhtml')
    itemref_insert('API/core/lv_obj_class_private_h.xhtml')
    itemref_insert('API/core/lv_obj_draw_h.xhtml')
    itemref_insert('API/core/lv_obj_draw_private_h.xhtml')
    itemref_insert('API/core/lv_obj_event_h.xhtml')
    itemref_insert('API/core/lv_obj_event_private_h.xhtml')
    itemref_insert('API/core/lv_obj_pos_h.xhtml')
    itemref_insert('API/core/lv_obj_private_h.xhtml')
    itemref_insert('API/core/lv_obj_scroll_h.xhtml')
    itemref_insert('API/core/lv_obj_scroll_private_h.xhtml')
    itemref_insert('API/core/lv_obj_style_h.xhtml')
    itemref_insert('API/core/lv_obj_style_gen_h.xhtml')
    itemref_insert('API/core/lv_obj_style_private_h.xhtml')
    itemref_insert('API/core/lv_obj_tree_h.xhtml')
    itemref_insert('API/core/lv_observer_h.xhtml')
    itemref_insert('API/core/lv_observer_private_h.xhtml')
    itemref_insert('API/core/lv_refr_h.xhtml')
    itemref_insert('API/core/lv_refr_private_h.xhtml')


    itemref_insert('API/debugging/index.xhtml')

    itemref_insert('API/debugging/monkey/index.xhtml')
    itemref_insert('API/debugging/monkey/lv_monkey_h.xhtml')
    itemref_insert('API/debugging/monkey/lv_monkey_private_h.xhtml')

    itemref_insert('API/debugging/sysmon/index.xhtml')
    itemref_insert('API/debugging/sysmon/lv_sysmon_h.xhtml')
    itemref_insert('API/debugging/sysmon/lv_sysmon_private_h.xhtml')

    itemref_insert('API/debugging/test/index.xhtml')
    itemref_insert('API/debugging/test/lv_test_h.xhtml')
    itemref_insert('API/debugging/test/lv_test_display_h.xhtml')
    itemref_insert('API/debugging/test/lv_test_fs_h.xhtml')
    itemref_insert('API/debugging/test/lv_test_helpers_h.xhtml')
    itemref_insert('API/debugging/test/lv_test_indev_h.xhtml')
    itemref_insert('API/debugging/test/lv_test_indev_gesture_h.xhtml')
    itemref_insert('API/debugging/test/lv_test_private_h.xhtml')
    itemref_insert('API/debugging/test/lv_test_screenshot_compare_h.xhtml')

    itemref_insert('API/display/index.xhtml')
    itemref_insert('API/display/lv_display_h.xhtml')
    itemref_insert('API/display/lv_display_private_h.xhtml')

    itemref_insert('API/draw/index.xhtml')
    itemref_insert('API/draw/lv_draw_h.xhtml')
    itemref_insert('API/draw/lv_draw_3d_h.xhtml')
    itemref_insert('API/draw/lv_draw_arc_h.xhtml')
    itemref_insert('API/draw/lv_draw_blur_h.xhtml')
    itemref_insert('API/draw/lv_draw_buf_h.xhtml')
    itemref_insert('API/draw/lv_draw_buf_private_h.xhtml')
    itemref_insert('API/draw/lv_draw_image_h.xhtml')
    itemref_insert('API/draw/lv_draw_image_private_h.xhtml')
    itemref_insert('API/draw/lv_draw_label_h.xhtml')
    itemref_insert('API/draw/lv_draw_label_private_h.xhtml')
    itemref_insert('API/draw/lv_draw_line_h.xhtml')
    itemref_insert('API/draw/lv_draw_mask_h.xhtml')
    itemref_insert('API/draw/lv_draw_private_h.xhtml')
    itemref_insert('API/draw/lv_draw_rect_h.xhtml')
    itemref_insert('API/draw/lv_draw_rect_private_h.xhtml')
    itemref_insert('API/draw/lv_draw_triangle_h.xhtml')
    itemref_insert('API/draw/lv_draw_triangle_private_h.xhtml')
    itemref_insert('API/draw/lv_draw_vector_h.xhtml')
    itemref_insert('API/draw/lv_draw_vector_private_h.xhtml')
    itemref_insert('API/draw/lv_image_decoder_h.xhtml')
    itemref_insert('API/draw/lv_image_decoder_private_h.xhtml')
    itemref_insert('API/draw/lv_image_dsc_h.xhtml')

    itemref_insert('API/draw/convert/index.xhtml')

    itemref_insert('API/draw/convert/lv_draw_buf_convert_h.xhtml')

    itemref_insert('API/draw/convert/helium/index.xhtml')
    itemref_insert('API/draw/convert/helium/lv_draw_buf_convert_helium_h.xhtml')

    itemref_insert('API/draw/convert/neon/index.xhtml')
    itemref_insert('API/draw/convert/neon/lv_draw_buf_convert_neon_h.xhtml')

    itemref_insert('API/draw/dma2d/index.xhtml')
    itemref_insert('API/draw/dma2d/lv_draw_dma2d_h.xhtml')
    itemref_insert('API/draw/dma2d/lv_draw_dma2d_private_h.xhtml')

    itemref_insert('API/draw/espressif/index.xhtml')

    itemref_insert('API/draw/espressif/ppa/index.xhtml')
    itemref_insert('API/draw/espressif/ppa/lv_draw_ppa_h.xhtml')
    itemref_insert('API/draw/espressif/ppa/lv_draw_ppa_private_h.xhtml')

    itemref_insert('API/draw/eve/index.xhtml')
    itemref_insert('API/draw/eve/lv_draw_eve_h.xhtml')
    itemref_insert('API/draw/eve/lv_draw_eve_private_h.xhtml')
    itemref_insert('API/draw/eve/lv_draw_eve_ram_g_h.xhtml')
    itemref_insert('API/draw/eve/lv_draw_eve_target_h.xhtml')
    itemref_insert('API/draw/eve/lv_eve_h.xhtml')

    itemref_insert('API/draw/nanovg/index.xhtml')
    itemref_insert('API/draw/nanovg/lv_draw_nanovg_h.xhtml')
    itemref_insert('API/draw/nanovg/lv_draw_nanovg_private_h.xhtml')
    itemref_insert('API/draw/nanovg/lv_nanovg_fbo_cache_h.xhtml')
    itemref_insert('API/draw/nanovg/lv_nanovg_image_cache_h.xhtml')
    itemref_insert('API/draw/nanovg/lv_nanovg_math_h.xhtml')
    itemref_insert('API/draw/nanovg/lv_nanovg_utils_h.xhtml')

    itemref_insert('API/draw/nema_gfx/index.xhtml')
    itemref_insert('API/draw/nema_gfx/lv_draw_nema_gfx_h.xhtml')
    itemref_insert('API/draw/nema_gfx/lv_draw_nema_gfx_utils_h.xhtml')
    itemref_insert('API/draw/nema_gfx/lv_nema_gfx_path_h.xhtml')

    itemref_insert('API/draw/nxp/index.xhtml')

    itemref_insert('API/draw/nxp/g2d/index.xhtml')
    itemref_insert('API/draw/nxp/g2d/lv_draw_g2d_h.xhtml')
    itemref_insert('API/draw/nxp/g2d/lv_g2d_buf_map_h.xhtml')
    itemref_insert('API/draw/nxp/g2d/lv_g2d_utils_h.xhtml')

    itemref_insert('API/draw/nxp/pxp/index.xhtml')
    itemref_insert('API/draw/nxp/pxp/lv_draw_pxp_h.xhtml')
    itemref_insert('API/draw/nxp/pxp/lv_pxp_cfg_h.xhtml')
    itemref_insert('API/draw/nxp/pxp/lv_pxp_osa_h.xhtml')
    itemref_insert('API/draw/nxp/pxp/lv_pxp_utils_h.xhtml')

    itemref_insert('API/draw/opengles/index.xhtml')
    itemref_insert('API/draw/opengles/lv_draw_opengles_h.xhtml')

    itemref_insert('API/draw/renesas/index.xhtml')

    itemref_insert('API/draw/renesas/dave2d/index.xhtml')
    itemref_insert('API/draw/renesas/dave2d/lv_draw_dave2d_h.xhtml')
    itemref_insert('API/draw/renesas/dave2d/lv_draw_dave2d_utils_h.xhtml')

    itemref_insert('API/draw/sdl/index.xhtml')
    itemref_insert('API/draw/sdl/lv_draw_sdl_h.xhtml')

    itemref_insert('API/draw/snapshot/index.xhtml')
    itemref_insert('API/draw/snapshot/lv_snapshot_h.xhtml')

    itemref_insert('API/draw/sw/index.xhtml')
    itemref_insert('API/draw/sw/lv_draw_sw_h.xhtml')
    itemref_insert('API/draw/sw/lv_draw_sw_grad_h.xhtml')
    itemref_insert('API/draw/sw/lv_draw_sw_mask_h.xhtml')
    itemref_insert('API/draw/sw/lv_draw_sw_mask_private_h.xhtml')
    itemref_insert('API/draw/sw/lv_draw_sw_private_h.xhtml')
    itemref_insert('API/draw/sw/lv_draw_sw_utils_h.xhtml')

    itemref_insert('API/draw/sw/arm2d/index.xhtml')
    itemref_insert('API/draw/sw/arm2d/lv_draw_sw_arm2d_h.xhtml')
    itemref_insert('API/draw/sw/arm2d/lv_draw_sw_helium_h.xhtml')

    itemref_insert('API/draw/sw/blend/index.xhtml')
    itemref_insert('API/draw/sw/blend/lv_draw_sw_blend_h.xhtml')
    itemref_insert('API/draw/sw/blend/lv_draw_sw_blend_private_h.xhtml')
    itemref_insert('API/draw/sw/blend/lv_draw_sw_blend_to_a8_h.xhtml')
    itemref_insert('API/draw/sw/blend/lv_draw_sw_blend_to_al88_h.xhtml')
    itemref_insert('API/draw/sw/blend/lv_draw_sw_blend_to_argb8888_h.xhtml')
    itemref_insert('API/draw/sw/blend/lv_draw_sw_blend_to_argb8888_premultiplied_h.xhtml')
    itemref_insert('API/draw/sw/blend/lv_draw_sw_blend_to_i1_h.xhtml')
    itemref_insert('API/draw/sw/blend/lv_draw_sw_blend_to_l8_h.xhtml')
    itemref_insert('API/draw/sw/blend/lv_draw_sw_blend_to_rgb565_h.xhtml')
    itemref_insert('API/draw/sw/blend/lv_draw_sw_blend_to_rgb565_swapped_h.xhtml')
    itemref_insert('API/draw/sw/blend/lv_draw_sw_blend_to_rgb888_h.xhtml')

    itemref_insert('API/draw/sw/blend/arm2d/index.xhtml')
    itemref_insert('API/draw/sw/blend/arm2d/lv_blend_arm2d_h.xhtml')

    itemref_insert('API/draw/sw/blend/helium/index.xhtml')
    itemref_insert('API/draw/sw/blend/helium/lv_blend_helium_h.xhtml')

    itemref_insert('API/draw/sw/blend/neon/index.xhtml')
    itemref_insert('API/draw/sw/blend/neon/lv_blend_neon_h.xhtml')
    itemref_insert('API/draw/sw/blend/neon/lv_draw_sw_blend_neon_to_rgb565_h.xhtml')
    itemref_insert('API/draw/sw/blend/neon/lv_draw_sw_blend_neon_to_rgb888_h.xhtml')

    itemref_insert('API/draw/sw/blend/riscv_v/index.xhtml')
    itemref_insert('API/draw/sw/blend/riscv_v/lv_blend_riscv_v_h.xhtml')
    itemref_insert('API/draw/sw/blend/riscv_v/lv_blend_riscv_v_private_h.xhtml')
    itemref_insert('API/draw/sw/blend/riscv_v/lv_blend_riscv_vector_emulation_h.xhtml')
    itemref_insert('API/draw/sw/blend/riscv_v/lv_draw_sw_blend_riscv_v_to_rgb888_h.xhtml')


    itemref_insert('API/draw/vg_lite/index.xhtml')
    itemref_insert('API/draw/vg_lite/lv_draw_vg_lite_h.xhtml')
    itemref_insert('API/draw/vg_lite/lv_draw_vg_lite_type_h.xhtml')
    itemref_insert('API/draw/vg_lite/lv_vg_lite_bitmap_font_cache_h.xhtml')
    itemref_insert('API/draw/vg_lite/lv_vg_lite_decoder_h.xhtml')
    itemref_insert('API/draw/vg_lite/lv_vg_lite_grad_h.xhtml')
    itemref_insert('API/draw/vg_lite/lv_vg_lite_math_h.xhtml')
    itemref_insert('API/draw/vg_lite/lv_vg_lite_path_h.xhtml')
    itemref_insert('API/draw/vg_lite/lv_vg_lite_pending_h.xhtml')
    itemref_insert('API/draw/vg_lite/lv_vg_lite_stroke_h.xhtml')
    itemref_insert('API/draw/vg_lite/lv_vg_lite_utils_h.xhtml')


    itemref_insert('API/drivers/index.xhtml')
    itemref_insert('API/drivers/lv_drivers_h.xhtml')

    itemref_insert('API/drivers/display/index.xhtml')

    itemref_insert('API/drivers/display/drm/index.xhtml')
    itemref_insert('API/drivers/display/drm/lv_linux_drm_h.xhtml')
    itemref_insert('API/drivers/display/drm/lv_linux_drm_egl_private_h.xhtml')

    itemref_insert('API/drivers/display/fb/index.xhtml')
    itemref_insert('API/drivers/display/fb/lv_linux_fbdev_h.xhtml')

    itemref_insert('API/drivers/display/ft81x/index.xhtml')
    itemref_insert('API/drivers/display/ft81x/lv_ft81x_h.xhtml')
    itemref_insert('API/drivers/display/ft81x/lv_ft81x_defines_h.xhtml')

    itemref_insert('API/drivers/display/ili9341/index.xhtml')
    itemref_insert('API/drivers/display/ili9341/lv_ili9341_h.xhtml')

    itemref_insert('API/drivers/display/lcd/index.xhtml')
    itemref_insert('API/drivers/display/lcd/lv_lcd_generic_mipi_h.xhtml')

    itemref_insert('API/drivers/display/lovyan_gfx/index.xhtml')
    itemref_insert('API/drivers/display/lovyan_gfx/lv_lgfx_user_hpp.xhtml')
    itemref_insert('API/drivers/display/lovyan_gfx/lv_lovyan_gfx_h.xhtml')

    itemref_insert('API/drivers/display/nv3007/index.xhtml')
    itemref_insert('API/drivers/display/nv3007/lv_nv3007_h.xhtml')

    itemref_insert('API/drivers/display/nxp_elcdif/index.xhtml')
    itemref_insert('API/drivers/display/nxp_elcdif/lv_nxp_elcdif_h.xhtml')

    itemref_insert('API/drivers/display/renesas_glcdc/index.xhtml')
    itemref_insert('API/drivers/display/renesas_glcdc/lv_renesas_glcdc_h.xhtml')

    itemref_insert('API/drivers/display/st7735/index.xhtml')
    itemref_insert('API/drivers/display/st7735/lv_st7735_h.xhtml')

    itemref_insert('API/drivers/display/st7789/index.xhtml')
    itemref_insert('API/drivers/display/st7789/lv_st7789_h.xhtml')

    itemref_insert('API/drivers/display/st7796/index.xhtml')
    itemref_insert('API/drivers/display/st7796/lv_st7796_h.xhtml')

    itemref_insert('API/drivers/display/st_ltdc/index.xhtml')
    itemref_insert('API/drivers/display/st_ltdc/lv_st_ltdc_h.xhtml')

    itemref_insert('API/drivers/display/tft_espi/index.xhtml')
    itemref_insert('API/drivers/display/tft_espi/lv_tft_espi_h.xhtml')

    itemref_insert('API/drivers/draw/index.xhtml')

    itemref_insert('API/drivers/draw/eve/index.xhtml')
    itemref_insert('API/drivers/draw/eve/lv_draw_eve_display_h.xhtml')
    itemref_insert('API/drivers/draw/eve/lv_draw_eve_display_defines_h.xhtml')

    itemref_insert('API/drivers/evdev/index.xhtml')
    itemref_insert('API/drivers/evdev/lv_evdev_h.xhtml')
    itemref_insert('API/drivers/evdev/lv_evdev_private_h.xhtml')

    itemref_insert('API/drivers/libinput/index.xhtml')
    itemref_insert('API/drivers/libinput/lv_libinput_h.xhtml')
    itemref_insert('API/drivers/libinput/lv_libinput_private_h.xhtml')
    itemref_insert('API/drivers/libinput/lv_xkb_h.xhtml')
    itemref_insert('API/drivers/libinput/lv_xkb_private_h.xhtml')

    itemref_insert('API/drivers/nuttx/index.xhtml')
    itemref_insert('API/drivers/nuttx/lv_nuttx_cache_h.xhtml')
    itemref_insert('API/drivers/nuttx/lv_nuttx_entry_h.xhtml')
    itemref_insert('API/drivers/nuttx/lv_nuttx_fbdev_h.xhtml')
    itemref_insert('API/drivers/nuttx/lv_nuttx_image_cache_h.xhtml')
    itemref_insert('API/drivers/nuttx/lv_nuttx_lcd_h.xhtml')
    itemref_insert('API/drivers/nuttx/lv_nuttx_libuv_h.xhtml')
    itemref_insert('API/drivers/nuttx/lv_nuttx_mouse_h.xhtml')
    itemref_insert('API/drivers/nuttx/lv_nuttx_profiler_h.xhtml')
    itemref_insert('API/drivers/nuttx/lv_nuttx_touchscreen_h.xhtml')

    itemref_insert('API/drivers/opengles/index.xhtml')
    itemref_insert('API/drivers/opengles/lv_opengles_debug_h.xhtml')
    itemref_insert('API/drivers/opengles/lv_opengles_driver_h.xhtml')
    itemref_insert('API/drivers/opengles/lv_opengles_egl_h.xhtml')
    itemref_insert('API/drivers/opengles/lv_opengles_egl_private_h.xhtml')
    itemref_insert('API/drivers/opengles/lv_opengles_glfw_h.xhtml')
    itemref_insert('API/drivers/opengles/lv_opengles_private_h.xhtml')
    itemref_insert('API/drivers/opengles/lv_opengles_texture_h.xhtml')
    itemref_insert('API/drivers/opengles/lv_opengles_texture_private_h.xhtml')
    itemref_insert('API/drivers/opengles/lv_opengles_window_h.xhtml')

    itemref_insert('API/drivers/opengles/assets/index.xhtml')
    itemref_insert('API/drivers/opengles/assets/lv_opengles_shader_h.xhtml')

    itemref_insert('API/drivers/opengles/opengl_shader/index.xhtml')
    itemref_insert('API/drivers/opengles/opengl_shader/lv_opengl_shader_internal_h.xhtml')

    itemref_insert('API/drivers/qnx/index.xhtml')
    itemref_insert('API/drivers/qnx/lv_qnx_h.xhtml')

    itemref_insert('API/drivers/sdl/index.xhtml')
    itemref_insert('API/drivers/sdl/lv_sdl_keyboard_h.xhtml')
    itemref_insert('API/drivers/sdl/lv_sdl_mouse_h.xhtml')
    itemref_insert('API/drivers/sdl/lv_sdl_mousewheel_h.xhtml')
    itemref_insert('API/drivers/sdl/lv_sdl_private_h.xhtml')
    itemref_insert('API/drivers/sdl/lv_sdl_window_h.xhtml')

    itemref_insert('API/drivers/uefi/index.xhtml')
    itemref_insert('API/drivers/uefi/lv_uefi_h.xhtml')
    itemref_insert('API/drivers/uefi/lv_uefi_context_h.xhtml')
    itemref_insert('API/drivers/uefi/lv_uefi_display_h.xhtml')
    itemref_insert('API/drivers/uefi/lv_uefi_edk2_h.xhtml')
    itemref_insert('API/drivers/uefi/lv_uefi_gnu_efi_h.xhtml')
    itemref_insert('API/drivers/uefi/lv_uefi_indev_h.xhtml')
    itemref_insert('API/drivers/uefi/lv_uefi_private_h.xhtml')
    itemref_insert('API/drivers/uefi/lv_uefi_std_wrapper_h.xhtml')

    itemref_insert('API/drivers/wayland/index.xhtml')
    itemref_insert('API/drivers/wayland/lv_wayland_h.xhtml')
    itemref_insert('API/drivers/wayland/lv_wayland_private_h.xhtml')
    itemref_insert('API/drivers/wayland/lv_wl_backend_private_h.xhtml')
    itemref_insert('API/drivers/wayland/lv_wl_keyboard_h.xhtml')
    itemref_insert('API/drivers/wayland/lv_wl_pointer_h.xhtml')
    itemref_insert('API/drivers/wayland/lv_wl_pointer_axis_h.xhtml')
    itemref_insert('API/drivers/wayland/lv_wl_touch_h.xhtml')
    itemref_insert('API/drivers/wayland/lv_wl_window_h.xhtml')

    itemref_insert('API/drivers/windows/index.xhtml')
    itemref_insert('API/drivers/windows/lv_windows_context_h.xhtml')
    itemref_insert('API/drivers/windows/lv_windows_display_h.xhtml')
    itemref_insert('API/drivers/windows/lv_windows_input_h.xhtml')
    itemref_insert('API/drivers/windows/lv_windows_input_private_h.xhtml')

    itemref_insert('API/drivers/x11/index.xhtml')
    itemref_insert('API/drivers/x11/lv_x11_h.xhtml')

    itemref_insert('API/font/index.xhtml')
    itemref_insert('API/font/lv_font_h.xhtml')
    itemref_insert('API/font/lv_symbol_def_h.xhtml')

    itemref_insert('API/font/binfont_loader/index.xhtml')
    itemref_insert('API/font/binfont_loader/lv_binfont_loader_h.xhtml')

    itemref_insert('API/font/fmt_txt/index.xhtml')
    itemref_insert('API/font/fmt_txt/lv_font_fmt_txt_h.xhtml')
    itemref_insert('API/font/fmt_txt/lv_font_fmt_txt_private_h.xhtml')

    itemref_insert('API/font/font_manager/index.xhtml')
    itemref_insert('API/font/font_manager/lv_font_manager_h.xhtml')
    itemref_insert('API/font/font_manager/lv_font_manager_recycle_h.xhtml')

    itemref_insert('API/font/imgfont/index.xhtml')
    itemref_insert('API/font/imgfont/lv_imgfont_h.xhtml')

    itemref_insert('API/indev/index.xhtml')
    itemref_insert('API/indev/lv_gridnav_h.xhtml')
    itemref_insert('API/indev/lv_indev_h.xhtml')
    itemref_insert('API/indev/lv_indev_gesture_h.xhtml')
    itemref_insert('API/indev/lv_indev_gesture_private_h.xhtml')
    itemref_insert('API/indev/lv_indev_private_h.xhtml')
    itemref_insert('API/indev/lv_indev_scroll_h.xhtml')

    itemref_insert('API/layouts/index.xhtml')
    itemref_insert('API/layouts/lv_layout_h.xhtml')
    itemref_insert('API/layouts/lv_layout_private_h.xhtml')

    itemref_insert('API/layouts/flex/index.xhtml')
    itemref_insert('API/layouts/flex/lv_flex_h.xhtml')

    itemref_insert('API/layouts/grid/index.xhtml')
    itemref_insert('API/layouts/grid/lv_grid_h.xhtml')

    itemref_insert('API/libs/index.xhtml')

    itemref_insert('API/libs/barcode/index.xhtml')
    itemref_insert('API/libs/barcode/lv_barcode_h.xhtml')
    itemref_insert('API/libs/barcode/lv_barcode_private_h.xhtml')

    itemref_insert('API/libs/bin_decoder/index.xhtml')
    itemref_insert('API/libs/bin_decoder/lv_bin_decoder_h.xhtml')

    itemref_insert('API/libs/bmp/index.xhtml')
    itemref_insert('API/libs/bmp/lv_bmp_h.xhtml')

    itemref_insert('API/libs/ffmpeg/index.xhtml')
    itemref_insert('API/libs/ffmpeg/lv_ffmpeg_h.xhtml')
    itemref_insert('API/libs/ffmpeg/lv_ffmpeg_private_h.xhtml')

    itemref_insert('API/libs/freetype/index.xhtml')
    itemref_insert('API/libs/freetype/lv_freetype_h.xhtml')
    itemref_insert('API/libs/freetype/lv_freetype_private_h.xhtml')

    itemref_insert('API/libs/fsdrv/index.xhtml')
    itemref_insert('API/libs/fsdrv/lv_fsdrv_h.xhtml')

    itemref_insert('API/libs/gltf/index.xhtml')

    itemref_insert('API/libs/gltf/gltf_data/index.xhtml')
    itemref_insert('API/libs/gltf/gltf_data/lv_gltf_data_internal_h.xhtml')
    itemref_insert('API/libs/gltf/gltf_data/lv_gltf_data_internal_hpp.xhtml')
    itemref_insert('API/libs/gltf/gltf_data/lv_gltf_model_h.xhtml')
    itemref_insert('API/libs/gltf/gltf_data/lv_gltf_model_node_h.xhtml')

    itemref_insert('API/libs/gltf/gltf_environment/index.xhtml')
    itemref_insert('API/libs/gltf/gltf_environment/lv_gltf_environment_h.xhtml')
    itemref_insert('API/libs/gltf/gltf_environment/lv_gltf_environment_private_h.xhtml')

    itemref_insert('API/libs/gltf/gltf_view/index.xhtml')
    itemref_insert('API/libs/gltf/gltf_view/lv_gltf_h.xhtml')
    itemref_insert('API/libs/gltf/gltf_view/lv_gltf_view_internal_h.xhtml')

    itemref_insert('API/libs/gltf/gltf_view/assets/index.xhtml')
    itemref_insert('API/libs/gltf/gltf_view/assets/lv_gltf_view_shader_h.xhtml')

    itemref_insert('API/libs/gltf/math/index.xhtml')
    itemref_insert('API/libs/gltf/math/lv_3dmath_h.xhtml')
    itemref_insert('API/libs/gltf/math/lv_gltf_math_hpp.xhtml')

    itemref_insert('API/libs/gstreamer/index.xhtml')
    itemref_insert('API/libs/gstreamer/lv_gstreamer_h.xhtml')
    itemref_insert('API/libs/gstreamer/lv_gstreamer_internal_h.xhtml')

    itemref_insert('API/libs/libjpeg_turbo/index.xhtml')
    itemref_insert('API/libs/libjpeg_turbo/lv_libjpeg_turbo_h.xhtml')

    itemref_insert('API/libs/libpng/index.xhtml')
    itemref_insert('API/libs/libpng/lv_libpng_h.xhtml')

    itemref_insert('API/libs/libwebp/index.xhtml')
    itemref_insert('API/libs/libwebp/lv_libwebp_h.xhtml')

    itemref_insert('API/libs/lodepng/index.xhtml')
    itemref_insert('API/libs/lodepng/lv_lodepng_h.xhtml')

    itemref_insert('API/libs/qrcode/index.xhtml')
    itemref_insert('API/libs/qrcode/lv_qrcode_h.xhtml')
    itemref_insert('API/libs/qrcode/lv_qrcode_private_h.xhtml')

    itemref_insert('API/libs/rle/index.xhtml')
    itemref_insert('API/libs/rle/lv_rle_h.xhtml')

    itemref_insert('API/libs/rlottie/index.xhtml')
    itemref_insert('API/libs/rlottie/lv_rlottie_h.xhtml')
    itemref_insert('API/libs/rlottie/lv_rlottie_private_h.xhtml')

    itemref_insert('API/libs/svg/index.xhtml')
    itemref_insert('API/libs/svg/lv_svg_h.xhtml')
    itemref_insert('API/libs/svg/lv_svg_decoder_h.xhtml')
    itemref_insert('API/libs/svg/lv_svg_parser_h.xhtml')
    itemref_insert('API/libs/svg/lv_svg_render_h.xhtml')
    itemref_insert('API/libs/svg/lv_svg_token_h.xhtml')

    itemref_insert('API/libs/tiny_ttf/index.xhtml')
    itemref_insert('API/libs/tiny_ttf/lv_tiny_ttf_h.xhtml')

    itemref_insert('API/libs/tjpgd/index.xhtml')
    itemref_insert('API/libs/tjpgd/lv_tjpgd_h.xhtml')

    itemref_insert('API/misc/index.xhtml')
    itemref_insert('API/misc/lv_anim_h.xhtml')
    itemref_insert('API/misc/lv_anim_private_h.xhtml')
    itemref_insert('API/misc/lv_anim_timeline_h.xhtml')
    itemref_insert('API/misc/lv_anim_timeline_private_h.xhtml')
    itemref_insert('API/misc/lv_area_h.xhtml')
    itemref_insert('API/misc/lv_area_private_h.xhtml')
    itemref_insert('API/misc/lv_array_h.xhtml')
    itemref_insert('API/misc/lv_assert_h.xhtml')
    itemref_insert('API/misc/lv_async_h.xhtml')
    itemref_insert('API/misc/lv_bidi_h.xhtml')
    itemref_insert('API/misc/lv_bidi_private_h.xhtml')
    itemref_insert('API/misc/lv_circle_buf_h.xhtml')
    itemref_insert('API/misc/lv_color_h.xhtml')
    itemref_insert('API/misc/lv_color_op_h.xhtml')
    itemref_insert('API/misc/lv_color_op_private_h.xhtml')
    itemref_insert('API/misc/lv_event_h.xhtml')
    itemref_insert('API/misc/lv_event_private_h.xhtml')
    itemref_insert('API/misc/lv_ext_data_h.xhtml')
    itemref_insert('API/misc/lv_fs_h.xhtml')
    itemref_insert('API/misc/lv_fs_private_h.xhtml')
    itemref_insert('API/misc/lv_grad_h.xhtml')
    itemref_insert('API/misc/lv_iter_h.xhtml')
    itemref_insert('API/misc/lv_ll_h.xhtml')
    itemref_insert('API/misc/lv_log_h.xhtml')
    itemref_insert('API/misc/lv_lru_h.xhtml')
    itemref_insert('API/misc/lv_math_h.xhtml')
    itemref_insert('API/misc/lv_matrix_h.xhtml')
    itemref_insert('API/misc/lv_palette_h.xhtml')
    itemref_insert('API/misc/lv_pending_h.xhtml')
    itemref_insert('API/misc/lv_profiler_h.xhtml')
    itemref_insert('API/misc/lv_profiler_builtin_h.xhtml')
    itemref_insert('API/misc/lv_profiler_builtin_private_h.xhtml')
    itemref_insert('API/misc/lv_rb_h.xhtml')
    itemref_insert('API/misc/lv_rb_private_h.xhtml')
    itemref_insert('API/misc/lv_style_h.xhtml')
    itemref_insert('API/misc/lv_style_gen_h.xhtml')
    itemref_insert('API/misc/lv_style_private_h.xhtml')
    itemref_insert('API/misc/lv_templ_h.xhtml')
    itemref_insert('API/misc/lv_text_h.xhtml')
    itemref_insert('API/misc/lv_text_ap_h.xhtml')
    itemref_insert('API/misc/lv_text_private_h.xhtml')
    itemref_insert('API/misc/lv_timer_h.xhtml')
    itemref_insert('API/misc/lv_timer_private_h.xhtml')
    itemref_insert('API/misc/lv_tree_h.xhtml')
    itemref_insert('API/misc/lv_utils_h.xhtml')

    itemref_insert('API/misc/cache/index.xhtml')
    itemref_insert('API/misc/cache/lv_cache_h.xhtml')
    itemref_insert('API/misc/cache/lv_cache_entry_h.xhtml')
    itemref_insert('API/misc/cache/lv_cache_entry_private_h.xhtml')
    itemref_insert('API/misc/cache/lv_cache_private_h.xhtml')

    itemref_insert('API/misc/cache/class/index.xhtml')
    itemref_insert('API/misc/cache/class/lv_cache_class_h.xhtml')
    itemref_insert('API/misc/cache/class/lv_cache_lru_ll_h.xhtml')
    itemref_insert('API/misc/cache/class/lv_cache_lru_rb_h.xhtml')
    itemref_insert('API/misc/cache/class/lv_cache_sc_da_h.xhtml')

    itemref_insert('API/misc/cache/instance/index.xhtml')
    itemref_insert('API/misc/cache/instance/lv_cache_instance_h.xhtml')
    itemref_insert('API/misc/cache/instance/lv_image_cache_h.xhtml')
    itemref_insert('API/misc/cache/instance/lv_image_header_cache_h.xhtml')

    itemref_insert('API/osal/index.xhtml')
    itemref_insert('API/osal/lv_linux_h.xhtml')
    itemref_insert('API/osal/lv_os_h.xhtml')
    itemref_insert('API/osal/lv_os_none_h.xhtml')
    itemref_insert('API/osal/lv_os_private_h.xhtml')

    itemref_insert('API/others/index.xhtml')

    itemref_insert('API/others/file_explorer/index.xhtml')
    itemref_insert('API/others/file_explorer/lv_file_explorer_h.xhtml')
    itemref_insert('API/others/file_explorer/lv_file_explorer_private_h.xhtml')

    itemref_insert('API/others/fragment/index.xhtml')
    itemref_insert('API/others/fragment/lv_fragment_h.xhtml')
    itemref_insert('API/others/fragment/lv_fragment_private_h.xhtml')

    itemref_insert('API/others/translation/index.xhtml')
    itemref_insert('API/others/translation/lv_translation_h.xhtml')
    itemref_insert('API/others/translation/lv_translation_private_h.xhtml')

    itemref_insert('API/stdlib/index.xhtml')
    itemref_insert('API/stdlib/lv_mem_h.xhtml')
    itemref_insert('API/stdlib/lv_mem_private_h.xhtml')
    itemref_insert('API/stdlib/lv_sprintf_h.xhtml')
    itemref_insert('API/stdlib/lv_string_h.xhtml')

    itemref_insert('API/stdlib/builtin/index.xhtml')
    itemref_insert('API/stdlib/builtin/lv_tlsf_h.xhtml')
    itemref_insert('API/stdlib/builtin/lv_tlsf_private_h.xhtml')

    itemref_insert('API/themes/index.xhtml')
    itemref_insert('API/themes/lv_theme_h.xhtml')
    itemref_insert('API/themes/lv_theme_private_h.xhtml')

    itemref_insert('API/themes/default/index.xhtml')
    itemref_insert('API/themes/default/lv_theme_default_h.xhtml')

    itemref_insert('API/themes/mono/index.xhtml')
    itemref_insert('API/themes/mono/lv_theme_mono_h.xhtml')

    itemref_insert('API/themes/simple/index.xhtml')
    itemref_insert('API/themes/simple/lv_theme_simple_h.xhtml')

    itemref_insert('API/tick/index.xhtml')
    itemref_insert('API/tick/lv_tick_h.xhtml')
    itemref_insert('API/tick/lv_tick_private_h.xhtml')

    itemref_insert('API/widgets/index.xhtml')

    itemref_insert('API/widgets/3dtexture/index.xhtml')
    itemref_insert('API/widgets/3dtexture/lv_3dtexture_h.xhtml')
    itemref_insert('API/widgets/3dtexture/lv_3dtexture_private_h.xhtml')

    itemref_insert('API/widgets/animimage/index.xhtml')
    itemref_insert('API/widgets/animimage/lv_animimage_h.xhtml')
    itemref_insert('API/widgets/animimage/lv_animimage_private_h.xhtml')

    itemref_insert('API/widgets/arc/index.xhtml')
    itemref_insert('API/widgets/arc/lv_arc_h.xhtml')
    itemref_insert('API/widgets/arc/lv_arc_private_h.xhtml')

    itemref_insert('API/widgets/arclabel/index.xhtml')
    itemref_insert('API/widgets/arclabel/lv_arclabel_h.xhtml')
    itemref_insert('API/widgets/arclabel/lv_arclabel_private_h.xhtml')

    itemref_insert('API/widgets/bar/index.xhtml')
    itemref_insert('API/widgets/bar/lv_bar_h.xhtml')
    itemref_insert('API/widgets/bar/lv_bar_private_h.xhtml')

    itemref_insert('API/widgets/button/index.xhtml')
    itemref_insert('API/widgets/button/lv_button_h.xhtml')
    itemref_insert('API/widgets/button/lv_button_private_h.xhtml')

    itemref_insert('API/widgets/buttonmatrix/index.xhtml')
    itemref_insert('API/widgets/buttonmatrix/lv_buttonmatrix_h.xhtml')
    itemref_insert('API/widgets/buttonmatrix/lv_buttonmatrix_private_h.xhtml')

    itemref_insert('API/widgets/calendar/index.xhtml')
    itemref_insert('API/widgets/calendar/lv_calendar_h.xhtml')
    itemref_insert('API/widgets/calendar/lv_calendar_chinese_h.xhtml')
    itemref_insert('API/widgets/calendar/lv_calendar_header_arrow_h.xhtml')
    itemref_insert('API/widgets/calendar/lv_calendar_header_dropdown_h.xhtml')
    itemref_insert('API/widgets/calendar/lv_calendar_private_h.xhtml')

    itemref_insert('API/widgets/canvas/index.xhtml')
    itemref_insert('API/widgets/canvas/lv_canvas_h.xhtml')
    itemref_insert('API/widgets/canvas/lv_canvas_private_h.xhtml')

    itemref_insert('API/widgets/chart/index.xhtml')
    itemref_insert('API/widgets/chart/lv_chart_h.xhtml')
    itemref_insert('API/widgets/chart/lv_chart_private_h.xhtml')

    itemref_insert('API/widgets/checkbox/index.xhtml')
    itemref_insert('API/widgets/checkbox/lv_checkbox_h.xhtml')
    itemref_insert('API/widgets/checkbox/lv_checkbox_private_h.xhtml')

    itemref_insert('API/widgets/dropdown/index.xhtml')
    itemref_insert('API/widgets/dropdown/lv_dropdown_h.xhtml')
    itemref_insert('API/widgets/dropdown/lv_dropdown_private_h.xhtml')

    itemref_insert('API/widgets/gif/index.xhtml')
    itemref_insert('API/widgets/gif/lv_gif_h.xhtml')

    itemref_insert('API/widgets/image/index.xhtml')
    itemref_insert('API/widgets/image/lv_image_h.xhtml')
    itemref_insert('API/widgets/image/lv_image_private_h.xhtml')

    itemref_insert('API/widgets/imagebutton/index.xhtml')
    itemref_insert('API/widgets/imagebutton/lv_imagebutton_h.xhtml')
    itemref_insert('API/widgets/imagebutton/lv_imagebutton_private_h.xhtml')

    itemref_insert('API/widgets/ime/index.xhtml')
    itemref_insert('API/widgets/ime/lv_ime_pinyin_h.xhtml')
    itemref_insert('API/widgets/ime/lv_ime_pinyin_private_h.xhtml')

    itemref_insert('API/widgets/keyboard/index.xhtml')
    itemref_insert('API/widgets/keyboard/lv_keyboard_h.xhtml')
    itemref_insert('API/widgets/keyboard/lv_keyboard_private_h.xhtml')

    itemref_insert('API/widgets/label/index.xhtml')
    itemref_insert('API/widgets/label/lv_label_h.xhtml')
    itemref_insert('API/widgets/label/lv_label_private_h.xhtml')

    itemref_insert('API/widgets/led/index.xhtml')
    itemref_insert('API/widgets/led/lv_led_h.xhtml')
    itemref_insert('API/widgets/led/lv_led_private_h.xhtml')

    itemref_insert('API/widgets/line/index.xhtml')
    itemref_insert('API/widgets/line/lv_line_h.xhtml')
    itemref_insert('API/widgets/line/lv_line_private_h.xhtml')

    itemref_insert('API/widgets/list/index.xhtml')
    itemref_insert('API/widgets/list/lv_list_h.xhtml')

    itemref_insert('API/widgets/lottie/index.xhtml')
    itemref_insert('API/widgets/lottie/lv_lottie_h.xhtml')
    itemref_insert('API/widgets/lottie/lv_lottie_private_h.xhtml')

    itemref_insert('API/widgets/menu/index.xhtml')
    itemref_insert('API/widgets/menu/lv_menu_h.xhtml')
    itemref_insert('API/widgets/menu/lv_menu_private_h.xhtml')

    itemref_insert('API/widgets/msgbox/index.xhtml')
    itemref_insert('API/widgets/msgbox/lv_msgbox_h.xhtml')
    itemref_insert('API/widgets/msgbox/lv_msgbox_private_h.xhtml')

    itemref_insert('API/widgets/objx_templ/index.xhtml')
    itemref_insert('API/widgets/objx_templ/lv_objx_templ_h.xhtml')

    itemref_insert('API/widgets/property/index.xhtml')
    itemref_insert('API/widgets/property/lv_obj_property_names_h.xhtml')
    itemref_insert('API/widgets/property/lv_style_properties_h.xhtml')

    itemref_insert('API/widgets/roller/index.xhtml')
    itemref_insert('API/widgets/roller/lv_roller_h.xhtml')
    itemref_insert('API/widgets/roller/lv_roller_private_h.xhtml')

    itemref_insert('API/widgets/scale/index.xhtml')
    itemref_insert('API/widgets/scale/lv_scale_h.xhtml')
    itemref_insert('API/widgets/scale/lv_scale_private_h.xhtml')

    itemref_insert('API/widgets/slider/index.xhtml')
    itemref_insert('API/widgets/slider/lv_slider_h.xhtml')
    itemref_insert('API/widgets/slider/lv_slider_private_h.xhtml')

    itemref_insert('API/widgets/span/index.xhtml')
    itemref_insert('API/widgets/span/lv_span_h.xhtml')
    itemref_insert('API/widgets/span/lv_span_private_h.xhtml')

    itemref_insert('API/widgets/spinbox/index.xhtml')
    itemref_insert('API/widgets/spinbox/lv_spinbox_h.xhtml')
    itemref_insert('API/widgets/spinbox/lv_spinbox_private_h.xhtml')

    itemref_insert('API/widgets/spinner/index.xhtml')
    itemref_insert('API/widgets/spinner/lv_spinner_h.xhtml')
    itemref_insert('API/widgets/spinner/lv_spinner_private_h.xhtml')

    itemref_insert('API/widgets/switch/index.xhtml')
    itemref_insert('API/widgets/switch/lv_switch_h.xhtml')
    itemref_insert('API/widgets/switch/lv_switch_private_h.xhtml')

    itemref_insert('API/widgets/table/index.xhtml')
    itemref_insert('API/widgets/table/lv_table_h.xhtml')
    itemref_insert('API/widgets/table/lv_table_private_h.xhtml')

    itemref_insert('API/widgets/tabview/index.xhtml')
    itemref_insert('API/widgets/tabview/lv_tabview_h.xhtml')
    itemref_insert('API/widgets/tabview/lv_tabview_private_h.xhtml')

    itemref_insert('API/widgets/textarea/index.xhtml')
    itemref_insert('API/widgets/textarea/lv_textarea_h.xhtml')
    itemref_insert('API/widgets/textarea/lv_textarea_private_h.xhtml')

    itemref_insert('API/widgets/tileview/index.xhtml')
    itemref_insert('API/widgets/tileview/lv_tileview_h.xhtml')
    itemref_insert('API/widgets/tileview/lv_tileview_private_h.xhtml')

    itemref_insert('API/widgets/win/index.xhtml')
    itemref_insert('API/widgets/win/lv_win_h.xhtml')
    itemref_insert('API/widgets/win/lv_win_private_h.xhtml')



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

