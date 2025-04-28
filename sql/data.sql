-- 插入用户数据
alter table user auto_increment = 1;

INSERT INTO `user` (`password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `nickname`, `gender`, `phone`, `is_ban`, `role`)
VALUES
('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 1, 'admin', '管理员', '李', 'admin@example.com', 1, 1, '2025-02-23 10:00:00', '超级管理员', 1, '13812345678', 0, 'admin'),
('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'wangkaiwen', '王凯文', '王', 'xiaoming@example.com', 1, 1, '2025-02-22 15:30:00', '凯文', 1, '13887654321', 0, 'general'),
('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'zhaoshanshan', '赵珊珊', '赵', 'xiaohong@example.com', 1, 1, '2025-02-21 14:00:00', '珊珊', 0, '13912345678', 0, 'general'),
('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'chenchenxi', '陈晨曦', '陈', 'lisa@example.com', 1, 1, '2025-02-20 09:00:00', '晨曦', 0, '13987654321', 0, 'general'),
('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'zhangweibo', '张伟博', '张', 'jerry@example.com', 1, 1, '2025-02-19 08:30:00', '伟博', 1, '13712345678', 0, 'general'),
('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'liujingyi', '刘婧怡', '刘', 'peter@example.com', 1, 1, '2025-02-18 07:45:00', '婧怡', 1, '13787654321', 0, 'general'),
('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'huangziqi', '黄子琪', '黄', 'lily@example.com', 1, 1, '2025-02-17 10:15:00', '子琪', 1, '13612345678', 0, 'designer'),
('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'yangfangyu', '杨芳瑜', '杨', 'tom@example.com', 1, 1, '2025-02-16 12:00:00', '芳瑜', 0, '13687654321', 0, 'designer'),
('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'liujunjie', '刘俊杰', '刘', 'grace@example.com', 1, 1, '2025-02-15 11:00:00', '俊杰', 1, '13512345678', 0, 'designer'),
('pbkdf2_sha256$600000$ZGdcvUGyH5vutRzCm7pm4h$7HWM2FDNOThWuBqEYr3O+6UJyPcLAGiOKvirofTCQ3Q=', NULL, 0, 'zhouzixuan', '周子轩', '周', 'winston@example.com', 1, 1, '2025-02-14 10:30:00', '子轩', 0, '13587654321', 0, 'designer');

