/* SPDX-License-Identifier: GPL-2.0-or-later
 * Copyright 2005 Blender Foundation. All rights reserved. */

/** \file
 * \ingroup shdnodes
 */

#include "node_shader_util.hh"

#include "UI_interface.h"
#include "UI_resources.h"

/* **************** BUMP TO ROUGHNESS ******************** */

namespace blender::nodes::node_shader_bump_to_roughness_cc {

static void node_declare(NodeDeclarationBuilder &b)
{
  b.add_input<decl::Float>(N_("Strength"))
      .default_value(1.0f)
      .min(0.0f)
      .max(1.0f)
      .subtype(PROP_FACTOR);
  b.add_input<decl::Float>(N_("Distance")).default_value(1.0f).min(0.0f).max(1000.0f);
  b.add_input<decl::Float>(N_("Height"))
      .default_value(1.0f)
      .min(-1000.0f)
      .max(1000.0f)
      .hide_value();
  b.add_input<decl::Float>(N_("Height_dx")).default_value(1.0f).unavailable();
  b.add_input<decl::Float>(N_("Height_dy")).default_value(1.0f).unavailable();
  b.add_input<decl::Vector>(N_("Normal")).min(-1.0f).max(1.0f).hide_value();
  b.add_output<decl::Vector>(N_("Normal"));
}

static void node_shader_buts_bump(uiLayout *layout, bContext *UNUSED(C), PointerRNA *ptr)
{
  uiItemR(layout, ptr, "invert", UI_ITEM_R_SPLIT_EMPTY_NAME, nullptr, 0);
}

static int gpu_shader_bump_to_roughness(GPUMaterial *mat,
                           bNode *node,
                           bNodeExecData *UNUSED(execdata),
                           GPUNodeStack *in,
                           GPUNodeStack *out)
{
  //if (!in[2].link) {
  //  if (!in[5].link) {
  //    return GPU_link(mat, "world_normals_get", &out[0].link);
  //  }
  //  else {
  //    /* Actually running the bump code would normalize, but Cycles handles it as total no-op. */
  //    return GPU_link(mat, "vector_copy", in[5].link, &out[0].link);
  //  }
  //}

  //if (!in[5].link) {
  //  GPU_link(mat, "world_normals_get", &in[5].link);
  //}

  //float invert = (node->custom1) ? -1.0 : 1.0;

  return GPU_stack_link(
      mat, node, "node_bump_to_roughness", in, out);
}

}  // namespace blender::nodes::node_shader_bump_cc

/* node type definition */
void register_node_type_sh_bump_to_roughness()
{
  namespace file_ns = blender::nodes::node_shader_bump_to_roughness_cc;

  static bNodeType ntype;

  sh_node_type_base(&ntype, SH_NODE_BUMP_TO_ROUGHNESS, "Bump To Roughness", NODE_CLASS_SHADER);
  ntype.declare = file_ns::node_declare;
  //ntype.draw_buttons = file_ns::node_shader_buts_bump;
  //ntype.draw_buttons = file_ns::node_shader_buts_principled;
  //node_type_gpu(&ntype, file_ns::gpu_shader_bump_to_roughness);

  //node_type_init(&ntype, file_ns::node_shader_init_principled);
  node_type_size_preset(&ntype, NODE_SIZE_LARGE);
  node_type_gpu(&ntype, file_ns::gpu_shader_bump_to_roughness);
  //node_type_update(&ntype, file_ns::node_shader_update_principled);

  nodeRegisterType(&ntype);
}

