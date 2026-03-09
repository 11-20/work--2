/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50710
 Source Host           : localhost:3306
 Source Schema         : dj

 Target Server Type    : MySQL
 Target Server Version : 50710
 File Encoding         : 65001

 Date: 06/12/2023 15:47:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for per
-- ----------------------------
DROP TABLE IF EXISTS `per`;
CREATE TABLE `per`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parentId` int(11) NULL DEFAULT NULL COMMENT '父级ID',
  `perName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '权限名称',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '节点路径',
  `perUrl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '页面路径',
  `perIcon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '权限图标',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '权限' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of per
-- ----------------------------
INSERT INTO `per` VALUES (3, 0, '系统', '0', '/', 'd');
INSERT INTO `per` VALUES (4, 3, '用户中心', '0,3,', '', '');
INSERT INTO `per` VALUES (5, 4, '用户管理', '0,3,4', '/user/usermanage', '');
INSERT INTO `per` VALUES (6, 4, '角色管理', '0,3,4,', '/user/rolemanage', '');
INSERT INTO `per` VALUES (13, 3, '系统管理', '0,3,', '', '');
INSERT INTO `per` VALUES (15, 13, '权限设置', '0,3,13,', '/setting/permissionmanage', '');
INSERT INTO `per` VALUES (16, 3, '轮播图管理', '0,3', '', '');
INSERT INTO `per` VALUES (17, 16, '轮播图add', '0,3,16', '/add', '');
INSERT INTO `per` VALUES (18, 16, '轮播图删除', '0,3,16', '/des', '');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '角色名',
  `status` int(11) NULL DEFAULT NULL COMMENT '状态',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '角色' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (1, '管理员', 1, '1');
INSERT INTO `role` VALUES (2, '管理员2', 1, '1');
INSERT INTO `role` VALUES (3, '普通用户', 1, '123');
INSERT INTO `role` VALUES (5, 'put', 1, '');

-- ----------------------------
-- Table structure for role_per
-- ----------------------------
DROP TABLE IF EXISTS `role_per`;
CREATE TABLE `role_per`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `perId` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '权限ID',
  `roleId` int(11) NULL DEFAULT NULL COMMENT '角色ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 77 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '角色权限' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of role_per
-- ----------------------------
INSERT INTO `role_per` VALUES (52, '7', 1);
INSERT INTO `role_per` VALUES (53, '12', 1);
INSERT INTO `role_per` VALUES (54, '4', 1);
INSERT INTO `role_per` VALUES (55, '6', 1);
INSERT INTO `role_per` VALUES (56, '5', 1);
INSERT INTO `role_per` VALUES (69, '3', 1);
INSERT INTO `role_per` VALUES (74, '16', 2);
INSERT INTO `role_per` VALUES (75, '17', 2);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户头像',
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '手机号',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码',
  `sex` int(11) NULL DEFAULT NULL COMMENT '性别',
  `role_id` int(11) NULL DEFAULT NULL COMMENT '角色',
  `status` int(11) NULL DEFAULT NULL COMMENT '状态',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `is_super` int(11) NULL DEFAULT NULL COMMENT '是否超级管理员',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (14, 'put', '头像', '17628197242', '21312@qq.com', 'e10adc3949ba59abbe56e057f20f883e', 0, 1, 1, '密码 123456', 1);
INSERT INTO `user` VALUES (15, 'test', '', '19090909090', '19090909090@163.com', 'df780a97b7d6a8f779f14728bccd3c4c', 0, 2, 1, '密码 909090', 0);

SET FOREIGN_KEY_CHECKS = 1;
