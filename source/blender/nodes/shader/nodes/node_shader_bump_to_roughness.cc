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
   b.add_input<decl::Vector>(N_("Normal")).hide_value();
   b.add_input<decl::Vector>(N_("Tangent")).hide_value();

   b.add_input<decl::Float>(N_("b0_h")).default_value(1.0f).hide_value();
   b.add_input<decl::Float>(N_("b1_dhds")).default_value(1.0f).hide_value();
   b.add_input<decl::Float>(N_("b2_dhdt")).default_value(1.0f).hide_value();
   b.add_input<decl::Float>(N_("b3_dhds2")).default_value(1.0f).hide_value();
   b.add_input<decl::Float>(N_("b4_dhdt2")).default_value(1.0f).hide_value();
   b.add_input<decl::Float>(N_("b5_dh2dsdt")).default_value(1.0f).hide_value();

      //b.add_input<decl::Int>(N_("invertBumpNormal"))
      // .default_value(0)
      // .min(0)
      // .max(1)
      // .subtype(PROP_FACTOR);

    b.add_input<decl::Float>(N_("invertBumpNormal"))
    .default_value(0.0f)
    .min(0.0f)
    .max(1.0f)
    .subtype(PROP_FACTOR);

    b.add_input<decl::Float>(N_("invertedBumpGain"))
    .default_value(-0.15f)
    .min(-1.0f)
    .max(1.0f)
    .subtype(PROP_FACTOR);

   //b.add_input<decl::Bool>(N_("invertBumpNormal")).default_value(false);
   b.add_input<decl::Float>(N_("baseRoughness"))
       .default_value(0.001f)
       .min(0.0f)
       .max(1.0f)
       .subtype(PROP_FACTOR);

   b.add_input<decl::Float>(N_("gain")).default_value(1.0f).min(0.0f).subtype(PROP_FACTOR);

   b.add_input<decl::Float>(N_("bumpNormalGain"))
       .default_value(1.0f)
       .min(0.0f)
       .subtype(PROP_FACTOR);

   b.add_input<decl::Float>(N_("anisotropyGain"))
       .default_value(1.0f)
       .min(0.0f)
       .subtype(PROP_FACTOR);

   b.add_output<decl::Vector>(N_("resultBumpNormal"));
   b.add_output<decl::Float>(N_("resultRoughness"));
   b.add_output<decl::Float>(N_("resultAnisotropy"));
   b.add_output<decl::Vector>(N_("resultAnisotropyDirection"));
}

static void node_shader_buts_bump_to_roughness(uiLayout *layout,
                                               bContext *UNUSED(C),
                                               PointerRNA *ptr)
{
  // uiItemR(layout, ptr, "invert", UI_ITEM_R_SPLIT_EMPTY_NAME, nullptr, 0);
}

static int gpu_shader_bump_to_roughness(GPUMaterial *mat,
                                        bNode *node,
                                        bNodeExecData *UNUSED(execdata),
                                        GPUNodeStack *in,
                                        GPUNodeStack *out)
{
  if (!in[0].link) {
     GPU_link(mat, "world_normals_get", &out[0].link);
   }

  return GPU_stack_link(mat, node, "node_bump_to_roughness", in, out);
}

static void node_shader_update_bump_to_roughness(bNodeTree *ntree, bNode *node)
{
  //const int distribution = node->custom1;
  //const int sss_method = node->custom2;

  LISTBASE_FOREACH (bNodeSocket *, sock, &node->inputs) {
    //if (STREQ(sock->name, "Transmission Roughness")) {
    //  nodeSetSocketAvailability(ntree, sock, distribution == SHD_GLOSSY_GGX);
    //}

    //if (STR_ELEM(sock->name, "Subsurface IOR", "Subsurface Anisotropy")) {
    //  nodeSetSocketAvailability(ntree, sock, sss_method != SHD_SUBSURFACE_BURLEY);
    //}
  }
}
static void node_shader_init_bump_to_roughness(bNodeTree *UNUSED(ntree), bNode *node)
{
}
}  // namespace blender::nodes::node_shader_bump_to_roughness_cc

void register_node_type_sh_bump_to_roughness()
{
  namespace file_ns = blender::nodes::node_shader_bump_to_roughness_cc;

  static bNodeType ntype;

  // sh_node_type_base(&ntype, SH_NODE_BUMP_TO_ROUGHNESS, "Bump To Roughness", NODE_CLASS_SHADER);
  // sh_node_type_base(&ntype, SH_NODE_BUMP_TO_ROUGHNESS, "Bump To Roughness",
  // NODE_CLASS_OP_VECTOR);
  sh_node_type_base(&ntype, SH_NODE_BUMP_TO_ROUGHNESS, "Bump To Roughness", NODE_CLASS_INPUT);
  ntype.declare = file_ns::node_declare;
  // ntype.draw_buttons = file_ns::node_shader_buts_bump;
  ntype.draw_buttons = file_ns::node_shader_buts_bump_to_roughness;
  // ntype.draw_buttons = file_ns::node_shader_buts_principled;
  // node_type_gpu(&ntype, file_ns::gpu_shader_bump_to_roughness);

  // node_type_init(&ntype, file_ns::node_shader_init_bump_to_roughness);
  node_type_size_preset(&ntype, NODE_SIZE_LARGE);
  node_type_gpu(&ntype, file_ns::gpu_shader_bump_to_roughness);
   node_type_update(&ntype, file_ns::node_shader_update_bump_to_roughness);

  nodeRegisterType(&ntype);
}
