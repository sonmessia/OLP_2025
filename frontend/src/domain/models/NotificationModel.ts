export interface NotificationModel {
  id: string;
  type: "error" | "warning" | "info" | "success";
  message: string;
  timestamp: Date;
}
