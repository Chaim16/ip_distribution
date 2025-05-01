-- 插入用户数据
alter table user auto_increment = 1;
INSERT INTO `user` VALUES ('pbkdf2_sha256$1000000$qbnVt7YLBZXFq57TqTr7aV$JVvy8mbDqo0v+fez6LTHefK6xMG7p2u3Lj11g+4VlPU=', NULL, 1, 'admin', '管理员', '李', 'admin@example.com', 1, 1, '2025-02-23 10:00:00.000000', 13, '超级管理员', 1, '13812345678', 0, 'administrator');
INSERT INTO `user` VALUES ('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'wangkaiwen', '王凯文', '王', 'xiaoming@example.com', 1, 1, '2025-02-22 15:30:00.000000', 14, '王凯文', 1, '13887654321', 0, 'general');
INSERT INTO `user` VALUES ('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'zhaoshanshan', '赵珊珊', '赵', 'xiaohong@example.com', 1, 1, '2025-02-21 14:00:00.000000', 15, '赵珊珊', 0, '13912345678', 0, 'general');
INSERT INTO `user` VALUES ('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'chenchenxi', '陈晨曦', '陈', 'lisa@example.com', 1, 1, '2025-02-20 09:00:00.000000', 16, '陈晨曦', 0, '13987654321', 0, 'general');
INSERT INTO `user` VALUES ('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'zhangweibo', '张伟博', '张', 'jerry@example.com', 1, 1, '2025-02-19 08:30:00.000000', 17, '张伟博', 1, '13712345678', 0, 'general');
INSERT INTO `user` VALUES ('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'liujingyi', '刘婧怡', '刘', 'peter@example.com', 1, 1, '2025-02-18 07:45:00.000000', 18, '刘婧怡', 1, '13787654321', 0, 'general');
INSERT INTO `user` VALUES ('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'huangziqi', '黄子琪', '黄', 'lily@example.com', 1, 1, '2025-02-17 10:15:00.000000', 19, '黄子琪', 1, '13612345678', 0, 'general');
INSERT INTO `user` VALUES ('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'yangfangyu', '杨芳瑜', '杨', 'tom@example.com', 1, 1, '2025-02-16 12:00:00.000000', 20, '杨芳瑜', 0, '13687654321', 0, 'general');
INSERT INTO `user` VALUES ('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'liujunjie', '刘俊杰', '刘', 'grace@example.com', 1, 1, '2025-02-15 11:00:00.000000', 21, '刘俊杰', 1, '13512345678', 0, 'general');
INSERT INTO `user` VALUES ('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'zhouzixuan', '周子轩', '周', 'winston@example.com', 1, 1, '2025-02-14 10:30:00.000000', 22, '周子轩', 0, '13587654321', 0, 'general');


-- ----------------------------
-- Records of router
-- ----------------------------
INSERT INTO `router` VALUES (1, '核心路由器-A1', 'Cisco ASR1001-X', '北京数据中心1楼', 8, 1746101094, 'admin');
INSERT INTO `router` VALUES (2, '边缘路由器-B2', 'Huawei AR1220E', '上海机房2楼', 4, 1746101110, 'admin');
INSERT INTO `router` VALUES (3, '骨干路由器-C3', 'Juniper MX204', '广州核心区3层', 10, 1746101124, 'admin');
INSERT INTO `router` VALUES (4, '接入路由器-D4', 'H3C R3600', '深圳科技园B座', 6, 1746101142, 'admin');
INSERT INTO `router` VALUES (5, '核心路由器-E5', 'Cisco ASR920', '成都IDC机房', 12, 1746101167, 'admin');



-- ----------------------------
-- Records of router_port
-- ----------------------------
INSERT INTO `router_port` VALUES (12, 'G/0', 1, '192.168.1.1', '192.168.1.10', '255.255.255.0', '192.168.1.254', '8.8.8.8', 1746101094, 'admin');
INSERT INTO `router_port` VALUES (13, 'G/1', 1, '192.168.1.11', '192.168.1.20', '255.255.255.0', '192.168.1.254', '8.8.8.8', 1746101094, 'admin');
INSERT INTO `router_port` VALUES (14, 'G/2', 1, '192.168.1.21', '192.168.1.30', '255.255.255.0', '192.168.1.254', '8.8.8.8', 1746101094, 'admin');
INSERT INTO `router_port` VALUES (15, 'G/3', 1, '192.168.1.31', '192.168.1.40', '255.255.255.0', '192.168.1.254', '8.8.8.8', 1746101094, 'admin');
INSERT INTO `router_port` VALUES (16, 'G/4', 1, '192.168.1.41', '192.168.1.50', '255.255.255.0', '192.168.1.254', '8.8.8.8', 1746101094, 'admin');
INSERT INTO `router_port` VALUES (17, 'G/5', 1, '192.168.1.51', '192.168.1.60', '255.255.255.0', '192.168.1.254', '8.8.8.8', 1746101094, 'admin');
INSERT INTO `router_port` VALUES (18, 'G/6', 1, '192.168.1.61', '192.168.1.70', '255.255.255.0', '192.168.1.254', '8.8.8.8', 1746101094, 'admin');
INSERT INTO `router_port` VALUES (19, 'G/7', 1, '192.168.1.71', '192.168.1.80', '255.255.255.0', '192.168.1.254', '8.8.8.8', 1746101094, 'admin');
INSERT INTO `router_port` VALUES (20, 'G/0', 2, '192.168.2.1', '192.168.2.10', '255.255.255.0', '192.168.2.254', '8.8.8.8', 1746101110, 'admin');
INSERT INTO `router_port` VALUES (21, 'G/1', 2, '192.168.2.11', '192.168.2.20', '255.255.255.0', '192.168.2.254', '8.8.8.8', 1746101110, 'admin');
INSERT INTO `router_port` VALUES (22, 'G/2', 2, '192.168.2.21', '192.168.2.30', '255.255.255.0', '192.168.2.254', '8.8.8.8', 1746101110, 'admin');
INSERT INTO `router_port` VALUES (23, 'G/3', 2, '192.168.2.31', '192.168.2.40', '255.255.255.0', '192.168.2.254', '8.8.8.8', 1746101110, 'admin');
INSERT INTO `router_port` VALUES (24, 'G/0', 3, '192.168.3.1', '192.168.3.10', '255.255.255.0', '192.168.3.254', '8.8.8.8', 1746101124, 'admin');
INSERT INTO `router_port` VALUES (25, 'G/1', 3, '192.168.3.11', '192.168.3.20', '255.255.255.0', '192.168.3.254', '8.8.8.8', 1746101124, 'admin');
INSERT INTO `router_port` VALUES (26, 'G/2', 3, '192.168.3.21', '192.168.3.30', '255.255.255.0', '192.168.3.254', '8.8.8.8', 1746101124, 'admin');
INSERT INTO `router_port` VALUES (27, 'G/3', 3, '192.168.3.31', '192.168.3.40', '255.255.255.0', '192.168.3.254', '8.8.8.8', 1746101124, 'admin');
INSERT INTO `router_port` VALUES (28, 'G/4', 3, '192.168.3.41', '192.168.3.50', '255.255.255.0', '192.168.3.254', '8.8.8.8', 1746101124, 'admin');
INSERT INTO `router_port` VALUES (29, 'G/5', 3, '192.168.3.51', '192.168.3.60', '255.255.255.0', '192.168.3.254', '8.8.8.8', 1746101124, 'admin');
INSERT INTO `router_port` VALUES (30, 'G/6', 3, '192.168.3.61', '192.168.3.70', '255.255.255.0', '192.168.3.254', '8.8.8.8', 1746101124, 'admin');
INSERT INTO `router_port` VALUES (31, 'G/7', 3, '192.168.3.71', '192.168.3.80', '255.255.255.0', '192.168.3.254', '8.8.8.8', 1746101124, 'admin');
INSERT INTO `router_port` VALUES (32, 'G/8', 3, '192.168.3.81', '192.168.3.90', '255.255.255.0', '192.168.3.254', '8.8.8.8', 1746101124, 'admin');
INSERT INTO `router_port` VALUES (33, 'G/9', 3, '192.168.3.91', '192.168.3.100', '255.255.255.0', '192.168.3.254', '8.8.8.8', 1746101124, 'admin');
INSERT INTO `router_port` VALUES (34, 'G/0', 4, '192.168.4.1', '192.168.4.10', '255.255.255.0', '192.168.4.254', '8.8.8.8', 1746101142, 'admin');
INSERT INTO `router_port` VALUES (35, 'G/1', 4, '192.168.4.11', '192.168.4.20', '255.255.255.0', '192.168.4.254', '8.8.8.8', 1746101142, 'admin');
INSERT INTO `router_port` VALUES (36, 'G/2', 4, '192.168.4.21', '192.168.4.30', '255.255.255.0', '192.168.4.254', '8.8.8.8', 1746101142, 'admin');
INSERT INTO `router_port` VALUES (37, 'G/3', 4, '192.168.4.31', '192.168.4.40', '255.255.255.0', '192.168.4.254', '8.8.8.8', 1746101142, 'admin');
INSERT INTO `router_port` VALUES (38, 'G/4', 4, '192.168.4.41', '192.168.4.50', '255.255.255.0', '192.168.4.254', '8.8.8.8', 1746101142, 'admin');
INSERT INTO `router_port` VALUES (39, 'G/5', 4, '192.168.4.51', '192.168.4.60', '255.255.255.0', '192.168.4.254', '8.8.8.8', 1746101142, 'admin');
INSERT INTO `router_port` VALUES (40, 'G/0', 5, '192.168.5.1', '192.168.5.10', '255.255.255.0', '192.168.5.254', '8.8.8.8', 1746101167, 'admin');
INSERT INTO `router_port` VALUES (41, 'G/1', 5, '192.168.5.11', '192.168.5.20', '255.255.255.0', '192.168.5.254', '8.8.8.8', 1746101167, 'admin');
INSERT INTO `router_port` VALUES (42, 'G/2', 5, '192.168.5.21', '192.168.5.30', '255.255.255.0', '192.168.5.254', '8.8.8.8', 1746101167, 'admin');
INSERT INTO `router_port` VALUES (43, 'G/3', 5, '192.168.5.31', '192.168.5.40', '255.255.255.0', '192.168.5.254', '8.8.8.8', 1746101167, 'admin');
INSERT INTO `router_port` VALUES (44, 'G/4', 5, '192.168.5.41', '192.168.5.50', '255.255.255.0', '192.168.5.254', '8.8.8.8', 1746101167, 'admin');
INSERT INTO `router_port` VALUES (45, 'G/5', 5, '192.168.5.51', '192.168.5.60', '255.255.255.0', '192.168.5.254', '8.8.8.8', 1746101167, 'admin');
INSERT INTO `router_port` VALUES (46, 'G/6', 5, '192.168.5.61', '192.168.5.70', '255.255.255.0', '192.168.5.254', '8.8.8.8', 1746101167, 'admin');
INSERT INTO `router_port` VALUES (47, 'G/7', 5, '192.168.5.71', '192.168.5.80', '255.255.255.0', '192.168.5.254', '8.8.8.8', 1746101167, 'admin');
INSERT INTO `router_port` VALUES (48, 'G/8', 5, '192.168.5.81', '192.168.5.90', '255.255.255.0', '192.168.5.254', '8.8.8.8', 1746101167, 'admin');
INSERT INTO `router_port` VALUES (49, 'G/9', 5, '192.168.5.91', '192.168.5.100', '255.255.255.0', '192.168.5.254', '8.8.8.8', 1746101167, 'admin');
INSERT INTO `router_port` VALUES (50, 'G/10', 5, '192.168.5.101', '192.168.5.110', '255.255.255.0', '192.168.5.254', '8.8.8.8', 1746101167, 'admin');


-- ----------------------------
-- Records of switch
-- ----------------------------
INSERT INTO `switch` VALUES (4, '研发部门交换机', 'Swich 01', 'Cisco Business 250', '研发区', 3, 24, 20, 1746113680, 'admin');
INSERT INTO `switch` VALUES (5, '销售部门交换机', 'Swich 02', 'Cisco Business 250', '销售办公区域', 3, 31, 20, 1746113747, 'admin');
INSERT INTO `switch` VALUES (6, 'HR部门交换机', 'Switch 03', 'TL-SG1024', 'HR办公区', 5, 40, 20, 1746114570, 'admin');
INSERT INTO `switch` VALUES (7, '安全部门交换机', 'Switch 04', 'N1100', '安全部门办公区域', 5, 41, 20, 1746114624, 'admin');


-- ----------------------------
-- Records of switch_port
-- ----------------------------
INSERT INTO `switch_port` VALUES (9, 4, NULL, '192.168.3.1');
INSERT INTO `switch_port` VALUES (10, 5, NULL, '192.168.3.71');
INSERT INTO `switch_port` VALUES (11, 5, NULL, '192.168.3.72');

-- ----------------------------
-- Records of workstation
-- ----------------------------
INSERT INTO `workstation` VALUES (8, 'dep-01', '研发部1楼1号', 9, 4, 16);
INSERT INTO `workstation` VALUES (9, 'sale-01', '销售部4楼1号', 10, 5, 16);
INSERT INTO `workstation` VALUES (10, 'sale-02', '销售部4楼2号', 11, 5, 17);
