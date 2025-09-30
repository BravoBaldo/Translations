.. Node-Red documentation master file, created by
   sphinx-quickstart on Sun Sep 28 17:52:44 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Node-Red documentation
======================

Developing Flows
================
Best practices for creating clear and reusable flows

.. toctree::
   :maxdepth: 2
   :caption: Developing Flows:

   ./docs/developing-flows/index.md
   ./docs/developing-flows/flow-structure.md
   ./docs/developing-flows/message-design.md
   ./docs/developing-flows/documenting-flows.md

   ./docs/user-guide/index.md
   ./docs/user-guide/concepts.md
   ./docs/user-guide/runtime/settings-file.md
   ./docs/user-guide/runtime/configuration.md
   ./docs/user-guide/runtime/securing-node-red.md
   ./docs/user-guide/runtime/logging.md
   ./docs/user-guide/projects/index.md
   ./docs/user-guide/runtime/adding-nodes.md
   ./docs/user-guide/runtime/embedding.md
   ./docs/user-guide/context.md
   ./docs/user-guide/environment-variables.md
   ./docs/user-guide/handling-errors.md
   ./docs/user-guide/messages.md
   ./docs/user-guide/node-red-admin.md
   ./docs/user-guide/nodes.md
   ./docs/user-guide/writing-functions.md
   ./docs/user-guide/editor/index.md
   ./docs/user-guide/editor/editors/buffer.md
   ./docs/user-guide/editor/editors/index.md
   ./docs/user-guide/editor/editors/js.md
   ./docs/user-guide/editor/editors/json.md
   ./docs/user-guide/editor/editors/jsonata.md
   ./docs/user-guide/editor/palette/index.md
   ./docs/user-guide/editor/palette/manager.md
   ./docs/user-guide/editor/settings/index.md
   ./docs/user-guide/editor/settings/keyboard.md
   ./docs/user-guide/editor/settings/view.md
   ./docs/user-guide/editor/sidebar/config.md
   ./docs/user-guide/editor/sidebar/context.md
   ./docs/user-guide/editor/sidebar/debug.md
   ./docs/user-guide/editor/sidebar/help.md
   ./docs/user-guide/editor/sidebar/index.md
   ./docs/user-guide/editor/sidebar/info.md
   ./docs/user-guide/editor/workspace/arrange.md
   ./docs/user-guide/editor/workspace/flows.md
   ./docs/user-guide/editor/workspace/groups.md
   ./docs/user-guide/editor/workspace/import-export.md
   ./docs/user-guide/editor/workspace/index.md
   ./docs/user-guide/editor/workspace/nodes.md
   ./docs/user-guide/editor/workspace/search.md
   ./docs/user-guide/editor/workspace/selection.md
   ./docs/user-guide/editor/workspace/subflows.md
   ./docs/user-guide/editor/workspace/wires.md
   
   ./docs/user-guide/images/context_change.png
   ./docs/user-guide/images/context_change_multiple_stores.png
   ./docs/user-guide/images/context_delete.png
   ./docs/user-guide/images/error_catch.png
   ./docs/user-guide/images/error_debug.png
   ./docs/user-guide/images/function_external_modules.png
   ./docs/user-guide/images/messages_change.png
   ./docs/user-guide/images/messages_debug.png
   ./docs/user-guide/images/messages_debug_detail.png
   ./docs/user-guide/images/messages_expr.png
   ./docs/user-guide/images/node_change.png
   ./docs/user-guide/images/node_debug.png
   ./docs/user-guide/images/node_function.png
   ./docs/user-guide/images/node_inject.png
   ./docs/user-guide/images/node_switch.png
   ./docs/user-guide/images/node_template.png
   
   ./docs/user-guide/projects/images/project_commit_history.png
   ./docs/user-guide/projects/images/project_dependencies.png
   ./docs/user-guide/projects/images/project_info_sidebar.png
   ./docs/user-guide/projects/images/project_local_changes.png
   ./docs/user-guide/projects/images/project_welcome.png

   ./docs/developing-flows/images/comment-nodes.png
   ./docs/developing-flows/images/debug-topic.png
   ./docs/developing-flows/images/grouping-nodes.png
   ./docs/developing-flows/images/link-nodes.png
   ./docs/developing-flows/images/mqtt-envvar.png
   ./docs/developing-flows/images/mqtt-query-save-id.png
   ./docs/developing-flows/images/mqtt-query.png
   ./docs/developing-flows/images/node-arrangement-sample-align.png
   ./docs/developing-flows/images/node-arrangement.png
   ./docs/developing-flows/images/node-output-labels.png
   ./docs/developing-flows/images/node-vertical-arrangement.png
   ./docs/developing-flows/images/placeholder.png
   ./docs/developing-flows/images/subflow-envvar.png
   ./docs/developing-flows/images/subflow-instance-envvar.png
   ./docs/developing-flows/images/subflow.png

   ./docs/user-guide/editor/images/delete-node-keep-wires.gif
   ./docs/user-guide/editor/images/detatch-node-from-wire.gif
   ./docs/user-guide/editor/images/editor-default-components.png
   ./docs/user-guide/editor/images/editor-default.png
   ./docs/user-guide/editor/images/editor-deploy-menu.png
   ./docs/user-guide/editor/images/editor-diff-flow.png
   ./docs/user-guide/editor/images/editor-edit-buffer-string.png
   ./docs/user-guide/editor/images/editor-edit-buffer.png
   ./docs/user-guide/editor/images/editor-edit-config-node.png
   ./docs/user-guide/editor/images/editor-edit-expression-func-ref.png
   ./docs/user-guide/editor/images/editor-edit-expression.png
   ./docs/user-guide/editor/images/editor-edit-flow.png
   ./docs/user-guide/editor/images/editor-edit-group-description.png
   ./docs/user-guide/editor/images/editor-edit-group.png
   ./docs/user-guide/editor/images/editor-edit-json.png
   ./docs/user-guide/editor/images/editor-edit-node-appearance.png
   ./docs/user-guide/editor/images/editor-edit-node-config-node.png
   ./docs/user-guide/editor/images/editor-edit-node-description.png
   ./docs/user-guide/editor/images/editor-edit-node-settings-icon.png
   ./docs/user-guide/editor/images/editor-edit-node.png
   ./docs/user-guide/editor/images/editor-edit-subflow-appearance.png
   ./docs/user-guide/editor/images/editor-edit-subflow-description.png
   ./docs/user-guide/editor/images/editor-edit-subflow-instance-node.png
   ./docs/user-guide/editor/images/editor-edit-subflow-module-properties.png
   ./docs/user-guide/editor/images/editor-edit-subflow-properties.png
   ./docs/user-guide/editor/images/editor-edit-subflow-property-ui.png
   ./docs/user-guide/editor/images/editor-edit-subflow-property.png
   ./docs/user-guide/editor/images/editor-edit-subflow.png
   ./docs/user-guide/editor/images/editor-export.png
   ./docs/user-guide/editor/images/editor-flow-search-tabs.png
   ./docs/user-guide/editor/images/editor-flow-select.png
   ./docs/user-guide/editor/images/editor-flow-tabs.png
   ./docs/user-guide/editor/images/editor-group.png
   ./docs/user-guide/editor/images/editor-import.png
   ./docs/user-guide/editor/images/editor-main-menu-export.png
   ./docs/user-guide/editor/images/editor-main-menu-import.png
   ./docs/user-guide/editor/images/editor-main-menu.png
   ./docs/user-guide/editor/images/editor-node-details.png
   ./docs/user-guide/editor/images/editor-node-hidden-label.png
   ./docs/user-guide/editor/images/editor-node-port-label.png
   ./docs/user-guide/editor/images/editor-node-wire.png
   ./docs/user-guide/editor/images/editor-palette-toggle.png
   ./docs/user-guide/editor/images/editor-palette.png
   ./docs/user-guide/editor/images/editor-quick-add.png
   ./docs/user-guide/editor/images/editor-search.png
   ./docs/user-guide/editor/images/editor-sidebar-config-nodes.png
   ./docs/user-guide/editor/images/editor-sidebar-context-copy.png
   ./docs/user-guide/editor/images/editor-sidebar-context-refresh.png
   ./docs/user-guide/editor/images/editor-sidebar-context.png
   ./docs/user-guide/editor/images/editor-sidebar-debug-filter.png
   ./docs/user-guide/editor/images/editor-sidebar-debug.png
   ./docs/user-guide/editor/images/editor-sidebar-help.png
   ./docs/user-guide/editor/images/editor-sidebar-info-entry.png
   ./docs/user-guide/editor/images/editor-sidebar-info.png
   ./docs/user-guide/editor/images/editor-sidebar-tab-picker.png
   ./docs/user-guide/editor/images/editor-sidebar.png
   ./docs/user-guide/editor/images/editor-subflow-create-selection.png
   ./docs/user-guide/editor/images/editor-subflow-invalid-selection.png
   ./docs/user-guide/editor/images/editor-typedInput-boolean.png
   ./docs/user-guide/editor/images/editor-typedInput-buffer.png
   ./docs/user-guide/editor/images/editor-typedInput-envvar-expanded.png
   ./docs/user-guide/editor/images/editor-typedInput-envvar.png
   ./docs/user-guide/editor/images/editor-typedInput-expression.png
   ./docs/user-guide/editor/images/editor-typedInput-flow-store.png
   ./docs/user-guide/editor/images/editor-typedInput-flow.png
   ./docs/user-guide/editor/images/editor-typedInput-global.png
   ./docs/user-guide/editor/images/editor-typedInput-json.png
   ./docs/user-guide/editor/images/editor-typedInput-msg.png
   ./docs/user-guide/editor/images/editor-typedInput-number.png
   ./docs/user-guide/editor/images/editor-typedInput-string.png
   ./docs/user-guide/editor/images/editor-typedInput.png
   ./docs/user-guide/editor/images/editor-user-login.png
   ./docs/user-guide/editor/images/editor-user-menu-2.png
   ./docs/user-guide/editor/images/editor-user-menu.png
   ./docs/user-guide/editor/images/editor-user-settings-keyboard-edit.png
   ./docs/user-guide/editor/images/editor-user-settings-keyboard.png
   ./docs/user-guide/editor/images/editor-user-settings-palette-install-details.png
   ./docs/user-guide/editor/images/editor-user-settings-palette-install.png
   ./docs/user-guide/editor/images/editor-user-settings-palette-nodes.png
   ./docs/user-guide/editor/images/editor-user-settings-view.png
   ./docs/user-guide/editor/images/editor-wiring-splice.png
   ./docs/user-guide/editor/images/editor-workspace-lasso.png
   ./docs/user-guide/editor/images/editor-workspace-navigator.png
   ./docs/user-guide/editor/images/select-multiple-wires.png
   
   ./docs/user-guide/editor/images/slicing-wires.gif
