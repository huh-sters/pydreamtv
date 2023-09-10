-- pydreamtv.channels definition

CREATE TABLE `channels` (
  `xui_id` bigint NOT NULL,
  `tvg_id` varchar(64) DEFAULT NULL,
  `tvg_name` varchar(100) DEFAULT NULL,
  `tvg_logo` varchar(255) DEFAULT NULL,
  `group_title` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `country` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`xui_id`),
  KEY `channels_tvg_id_IDX` (`tvg_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- pydreamtv.programmes definition

CREATE TABLE `programmes` (
  `start` datetime DEFAULT NULL,
  `stop` datetime DEFAULT NULL,
  `start_timestamp` bigint DEFAULT NULL,
  `stop_timestamp` bigint DEFAULT NULL,
  `channel` varchar(64) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `programmes_channel_IDX` (`channel`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
