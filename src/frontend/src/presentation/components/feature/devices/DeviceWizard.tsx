import React, { useState, useEffect } from "react";
import {
  DeviceType,
  ConnectionProtocol,
  DeviceFactory,
} from "../../../../domain/models/DeviceModels";
import type { DeviceModel } from "../../../../domain/models/DeviceModels";
import {
  Camera,
  Wind,
  Cpu,
  Wifi,
  Server,
  MapPin,
  CheckCircle,
  AlertCircle,
  Loader,
} from "lucide-react";

interface DeviceWizardProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (device: DeviceModel) => void;
  editingDevice?: DeviceModel;
}

type WizardStep = "type" | "connection" | "location" | "confirm";
type ConnectionTestResult = "idle" | "testing" | "success" | "error";

const deviceTypeOptions = [
  {
    type: DeviceType.TRAFFIC_CAM,
    title: "Camera Giao thông",
    description: "Đếm xe, nhận diện biển số, phát hiện ùn tắc",
    icon: Camera,
    color: "blue",
    protocol: ConnectionProtocol.RTSP,
  },
  {
    type: DeviceType.AIR_QUALITY_SENSOR,
    title: "Cảm biến Không khí",
    description: "Đo PM2.5, PM10, CO, NO2, nhiệt độ, độ ẩm",
    icon: Wind,
    color: "green",
    protocol: ConnectionProtocol.MQTT,
  },
  {
    type: DeviceType.SMART_LIGHT,
    title: "Đèn thông minh",
    description: "Điều khiển pha đèn giao thông",
    icon: Cpu,
    color: "purple",
    protocol: ConnectionProtocol.MQTT,
  },
  {
    type: DeviceType.INDUCTIVE_LOOP,
    title: "Cảm biến từ",
    description: "Đo lưu lượng và tốc độ xe",
    icon: Server,
    color: "orange",
    protocol: ConnectionProtocol.MQTT,
  },
];

const getStepNumber = (step: WizardStep): number => {
  switch (step) {
    case "type":
      return 1;
    case "connection":
      return 2;
    case "location":
      return 3;
    case "confirm":
      return 4;
    default:
      return 1;
  }
};

const getStepTitle = (step: WizardStep): string => {
  switch (step) {
    case "type":
      return "Chọn loại thiết bị";
    case "connection":
      return "Cấu hình kết nối";
    case "location":
      return "Định vị bản đồ";
    case "confirm":
      return "Xác nhận thông tin";
    default:
      return "";
  }
};

export const DeviceWizard: React.FC<DeviceWizardProps> = ({
  isOpen,
  onClose,
  onSubmit,
  editingDevice,
}) => {
  const [currentStep, setCurrentStep] = useState<WizardStep>("type");
  const [deviceData, setDeviceData] = useState<Partial<DeviceModel>>({
    name: "",
    type: DeviceType.TRAFFIC_CAM,
    protocol: ConnectionProtocol.MQTT,
    manufacturer: "",
    serialNumber: "",
    location: { latitude: 0, longitude: 0 },
    updateInterval: 30,
    isActive: true,
  });
  const [connectionTest, setConnectionTest] =
    useState<ConnectionTestResult>("idle");
  const [testError, setTestError] = useState<string>("");

  // Reset form khi mở modal
  useEffect(() => {
    if (isOpen) {
      if (editingDevice) {
        setDeviceData(editingDevice);
        setCurrentStep("confirm");
      } else {
        resetForm();
      }
    }
  }, [isOpen, editingDevice]);

  const resetForm = () => {
    setDeviceData({
      name: "",
      type: DeviceType.TRAFFIC_CAM,
      protocol: ConnectionProtocol.MQTT,
      manufacturer: "",
      serialNumber: "",
      location: { latitude: 0, longitude: 0 },
      updateInterval: 30,
      isActive: true,
    });
    setCurrentStep("type");
    setConnectionTest("idle");
    setTestError("");
  };

  const handleDeviceTypeSelect = (type: DeviceType) => {
    const selectedType = deviceTypeOptions.find((opt) => opt.type === type);
    setDeviceData({
      ...deviceData,
      type,
      protocol: selectedType?.protocol || ConnectionProtocol.MQTT,
    });
    setCurrentStep("connection");
  };

  const handleConnectionTest = async () => {
    setConnectionTest("testing");
    setTestError("");

    // Mock connection test - trong thực tế sẽ gọi API
    setTimeout(() => {
      const isSuccess = Math.random() > 0.2; // 80% success rate for demo

      if (isSuccess) {
        setConnectionTest("success");
      } else {
        setConnectionTest("error");
        setTestError(
          "Không thể kết nối đến thiết bị. Vui lòng kiểm tra lại cấu hình."
        );
      }
    }, 2000);
  };

  const handleLocationSelect = (lat: number, lng: number) => {
    setDeviceData({
      ...deviceData,
      location: { latitude: lat, longitude: lng },
    });
  };

  const handleNext = () => {
    switch (currentStep) {
      case "type":
        if (deviceData.type) setCurrentStep("connection");
        break;
      case "connection":
        setCurrentStep("location");
        break;
      case "location":
        setCurrentStep("confirm");
        break;
    }
  };

  const handleBack = () => {
    switch (currentStep) {
      case "connection":
        setCurrentStep("type");
        break;
      case "location":
        setCurrentStep("connection");
        break;
      case "confirm":
        setCurrentStep("location");
        break;
    }
  };

  const handleSubmit = () => {
    if (deviceData.type && deviceData.serialNumber && deviceData.location) {
      const newDevice = DeviceFactory.createTrafficCamera({
        ...deviceData,
        type: deviceData.type,
        serialNumber: deviceData.serialNumber,
        location: deviceData.location,
        id: editingDevice?.id || Date.now().toString(),
        createdAt: editingDevice?.createdAt || new Date(),
        updatedAt: new Date(),
      });
      onSubmit(newDevice);
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div className="bg-white dark:bg-gray-900 w-full max-w-4xl max-h-[90vh] overflow-hidden rounded-3xl border border-gray-200 dark:border-gray-700 shadow-2xl">
        {/* Header */}
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              {editingDevice ? "Chỉnh sửa thiết bị" : "Thêm thiết bị mới"}
            </h2>
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors text-gray-500 dark:text-gray-400"
            >
              ×
            </button>
          </div>

          {/* Progress Steps */}
          <div className="mt-6 flex items-center justify-between">
            {(
              ["type", "connection", "location", "confirm"] as WizardStep[]
            ).map((step) => (
              <div key={step} className="flex items-center flex-1">
                <div
                  className={`flex items-center justify-center w-10 h-10 rounded-full font-medium transition-colors ${
                    getStepNumber(currentStep) >= getStepNumber(step)
                      ? "bg-greenwave-primary-light text-white"
                      : "bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400"
                  }`}
                >
                  {getStepNumber(step)}
                </div>
                <span
                  className={`ml-3 text-sm font-medium transition-colors hidden md:block ${
                    getStepNumber(currentStep) >= getStepNumber(step)
                      ? "text-gray-900 dark:text-white"
                      : "text-gray-500 dark:text-gray-400"
                  }`}
                >
                  {getStepTitle(step)}
                </span>
                {step !== "confirm" && (
                  <div
                    className={`flex-1 h-1 mx-4 transition-colors ${
                      getStepNumber(currentStep) > getStepNumber(step)
                        ? "bg-greenwave-primary-light"
                        : "bg-gray-200 dark:bg-gray-700"
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto" style={{ maxHeight: "60vh" }}>
          {/* Step 1: Device Type Selection */}
          {currentStep === "type" && (
            <div>
              <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                Chọn loại thiết bị bạn muốn thêm
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {deviceTypeOptions.map((option) => {
                  const Icon = option.icon;
                  return (
                    <button
                      key={option.type}
                      onClick={() => handleDeviceTypeSelect(option.type)}
                      className={`p-6 rounded-2xl border-2 transition-all hover:scale-105 ${
                        deviceData.type === option.type
                          ? "border-greenwave-primary-light bg-green-50 dark:bg-green-900/20"
                          : "border-gray-200 dark:border-gray-700 hover:border-greenwave-primary-light/50 bg-white dark:bg-gray-800"
                      }`}
                    >
                      <div className="flex items-start gap-4">
                        <div
                          className={`p-3 rounded-lg bg-${option.color}-100 dark:bg-${option.color}-900/30`}
                        >
                          <Icon
                            className={`w-6 h-6 text-${option.color}-600 dark:text-${option.color}-400`}
                          />
                        </div>
                        <div className="text-left">
                          <h4 className="font-semibold text-gray-900 dark:text-white mb-1">
                            {option.title}
                          </h4>
                          <p className="text-sm text-gray-500 dark:text-gray-400">
                            {option.description}
                          </p>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Step 2: Connection Configuration */}
          {currentStep === "connection" && (
            <div>
              <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                Cấu hình kết nối thiết bị
              </h3>

              <div className="space-y-6">
                {/* General Information */}
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                    Thông tin chung
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                        Tên thiết bị *
                      </label>
                      <input
                        type="text"
                        value={deviceData.name || ""}
                        onChange={(e) =>
                          setDeviceData({ ...deviceData, name: e.target.value })
                        }
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                        placeholder="Ví dụ: Camera Ngã 4 Hàng Xanh"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                        Số serial *
                      </label>
                      <input
                        type="text"
                        value={deviceData.serialNumber || ""}
                        onChange={(e) =>
                          setDeviceData({
                            ...deviceData,
                            serialNumber: e.target.value,
                          })
                        }
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                        placeholder="SN-2024-X99"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                        Hãng sản xuất
                      </label>
                      <input
                        type="text"
                        value={deviceData.manufacturer || ""}
                        onChange={(e) =>
                          setDeviceData({
                            ...deviceData,
                            manufacturer: e.target.value,
                          })
                        }
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                        placeholder="Bosch, Honeywell..."
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                        Giao thức
                      </label>
                      <select
                        value={deviceData.protocol}
                        onChange={(e) =>
                          setDeviceData({
                            ...deviceData,
                            protocol: e.target.value as ConnectionProtocol,
                          })
                        }
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                      >
                        <option value={ConnectionProtocol.MQTT}>MQTT</option>
                        <option value={ConnectionProtocol.HTTP}>HTTP</option>
                        <option value={ConnectionProtocol.RTSP}>RTSP</option>
                        <option value={ConnectionProtocol.MODBUS_TCP}>
                          Modbus TCP
                        </option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Protocol-specific Configuration */}
                {deviceData.protocol === ConnectionProtocol.MQTT && (
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                      Cấu hình MQTT
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                          Broker URL
                        </label>
                        <input
                          type="text"
                          value={deviceData.mqttConfig?.brokerUrl || ""}
                          onChange={(e) =>
                            setDeviceData({
                              ...deviceData,
                              mqttConfig: {
                                ...deviceData.mqttConfig,
                                brokerUrl: e.target.value,
                              },
                            })
                          }
                          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                          placeholder="mqtt://broker.hivemq.com"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                          Cổng
                        </label>
                        <input
                          type="number"
                          value={deviceData.mqttConfig?.port || 1883}
                          onChange={(e) =>
                            setDeviceData({
                              ...deviceData,
                              mqttConfig: {
                                ...deviceData.mqttConfig,
                                port: parseInt(e.target.value),
                              },
                            })
                          }
                          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                          Topic Subscribe *
                        </label>
                        <input
                          type="text"
                          value={deviceData.mqttConfig?.topicSubscribe || ""}
                          onChange={(e) =>
                            setDeviceData({
                              ...deviceData,
                              mqttConfig: {
                                ...deviceData.mqttConfig,
                                topicSubscribe: e.target.value,
                              },
                            })
                          }
                          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                          placeholder="hcm/d1/hangxanh/traffic/data"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                          Topic Publish
                        </label>
                        <input
                          type="text"
                          value={deviceData.mqttConfig?.topicPublish || ""}
                          onChange={(e) =>
                            setDeviceData({
                              ...deviceData,
                              mqttConfig: {
                                ...deviceData.mqttConfig,
                                topicPublish: e.target.value,
                              },
                            })
                          }
                          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                          placeholder="hcm/d1/hangxanh/traffic/cmd"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {deviceData.protocol === ConnectionProtocol.RTSP && (
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                      Cấu hình RTSP
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                          Địa chỉ IP *
                        </label>
                        <input
                          type="text"
                          value={deviceData.httpConfig?.ipAddress || ""}
                          onChange={(e) =>
                            setDeviceData({
                              ...deviceData,
                              httpConfig: {
                                ...deviceData.httpConfig,
                                ipAddress: e.target.value,
                              },
                            })
                          }
                          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                          placeholder="192.168.1.105"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                          RTSP URL
                        </label>
                        <input
                          type="text"
                          value={deviceData.httpConfig?.rtspUrl || ""}
                          onChange={(e) =>
                            setDeviceData({
                              ...deviceData,
                              httpConfig: {
                                ...deviceData.httpConfig,
                                rtspUrl: e.target.value,
                              },
                            })
                          }
                          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                          placeholder="rtsp://admin:12345@192.168.1.105/stream"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* Connection Test */}
                <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white">
                        Kiểm tra kết nối
                      </h4>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                        Kiểm tra xem hệ thống có thể kết nối đến thiết bị không
                      </p>
                    </div>
                    <button
                      onClick={handleConnectionTest}
                      disabled={connectionTest === "testing"}
                      className="px-4 py-2 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                      style={{
                        background:
                          connectionTest === "success"
                            ? "var(--color-greenwave-primary-light)"
                            : connectionTest === "error"
                            ? "var(--color-traffic-red)"
                            : "linear-gradient(135deg, var(--color-greenwave-primary-light) 0%, var(--color-greenwave-primary-dark) 100%)",
                        color: "white",
                      }}
                    >
                      {connectionTest === "testing" && (
                        <Loader className="w-4 h-4 animate-spin" />
                      )}
                      {connectionTest === "success" && (
                        <CheckCircle className="w-4 h-4" />
                      )}
                      {connectionTest === "error" && (
                        <AlertCircle className="w-4 h-4" />
                      )}
                      {connectionTest === "idle" && (
                        <Wifi className="w-4 h-4" />
                      )}
                      {connectionTest === "testing"
                        ? "Đang kiểm tra..."
                        : "Kiểm tra kết nối"}
                    </button>
                  </div>

                  {connectionTest === "success" && (
                    <div className="mt-3 p-3 rounded-lg bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300">
                      ✓ Kết nối thành công! Thiết bị sẵn sàng để thêm vào hệ
                      thống.
                    </div>
                  )}

                  {connectionTest === "error" && testError && (
                    <div className="mt-3 p-3 rounded-lg bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300">
                      ✗ {testError}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Location */}
          {currentStep === "location" && (
            <div>
              <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                Định vị thiết bị trên bản đồ
              </h3>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                    Nhập tọa độ
                  </h4>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                        Vĩ độ (Latitude)
                      </label>
                      <input
                        type="number"
                        step="0.000001"
                        value={deviceData.location?.latitude || 0}
                        onChange={(e) =>
                          setDeviceData({
                            ...deviceData,
                            location: {
                              ...deviceData.location!,
                              latitude: parseFloat(e.target.value),
                            },
                          })
                        }
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                        placeholder="10.8231"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                        Kinh độ (Longitude)
                      </label>
                      <input
                        type="number"
                        step="0.000001"
                        value={deviceData.location?.longitude || 0}
                        onChange={(e) =>
                          setDeviceData({
                            ...deviceData,
                            location: {
                              ...deviceData.location!,
                              longitude: parseFloat(e.target.value),
                            },
                          })
                        }
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                        placeholder="106.6297"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                        Mô tả vị trí
                      </label>
                      <textarea
                        value={deviceData.location?.description || ""}
                        onChange={(e) =>
                          setDeviceData({
                            ...deviceData,
                            location: {
                              ...deviceData.location!,
                              description: e.target.value,
                            },
                          })
                        }
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-greenwave-primary-light"
                        placeholder="Cột đèn số 5, hướng về Quận 1"
                        rows={3}
                      />
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                    <MapPin className="inline w-4 h-4 mr-2" />
                    Chọn vị trí trên bản đồ
                  </h4>
                  <div className="p-4 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800/50 h-64 flex items-center justify-center">
                    <p className="text-gray-500 dark:text-gray-400 text-center">
                      <MapPin className="w-8 h-8 mx-auto mb-2" />
                      Bản đồ sẽ được tích hợp ở đây
                      <br />
                      <span className="text-sm">
                        Người dùng có thể kéo thả pin để chọn vị trí
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Step 4: Confirmation */}
          {currentStep === "confirm" && (
            <div>
              <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                Xác nhận thông tin thiết bị
              </h3>

              <div className="space-y-6">
                <div className="p-6 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                  <h4 className="font-medium text-gray-900 dark:text-white mb-4">
                    Thông tin chung
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <span className="text-sm text-gray-500 dark:text-gray-400">
                        Tên thiết bị:
                      </span>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {deviceData.name}
                      </p>
                    </div>
                    <div>
                      <span className="text-sm text-gray-500 dark:text-gray-400">
                        Loại thiết bị:
                      </span>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {deviceData.type}
                      </p>
                    </div>
                    <div>
                      <span className="text-sm text-gray-500 dark:text-gray-400">
                        Số serial:
                      </span>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {deviceData.serialNumber}
                      </p>
                    </div>
                    <div>
                      <span className="text-sm text-gray-500 dark:text-gray-400">
                        Hãng sản xuất:
                      </span>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {deviceData.manufacturer || "N/A"}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="p-6 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                  <h4 className="font-medium text-gray-900 dark:text-white mb-4">
                    Cấu hình kết nối
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <span className="text-sm text-gray-500 dark:text-gray-400">
                        Giao thức:
                      </span>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {deviceData.protocol}
                      </p>
                    </div>
                    {deviceData.mqttConfig && (
                      <div>
                        <span className="text-sm text-gray-500 dark:text-gray-400">
                          Topic MQTT:
                        </span>
                        <p className="font-medium text-gray-900 dark:text-white">
                          {deviceData.mqttConfig.topicSubscribe}
                        </p>
                      </div>
                    )}
                    {deviceData.httpConfig && (
                      <div>
                        <span className="text-sm text-gray-500 dark:text-gray-400">
                          Địa chỉ IP:
                        </span>
                        <p className="font-medium text-gray-900 dark:text-white">
                          {deviceData.httpConfig.ipAddress}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 flex justify-between">
          <button
            onClick={currentStep === "type" ? onClose : handleBack}
            className="px-6 py-2 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            {currentStep === "type" ? "Hủy" : "Quay lại"}
          </button>

          <button
            onClick={currentStep === "confirm" ? handleSubmit : handleNext}
            className="px-6 py-2 rounded-lg font-medium text-white transition-all hover:scale-105"
            style={{
              background:
                "linear-gradient(135deg, var(--color-greenwave-primary-light) 0%, var(--color-greenwave-primary-dark) 100%)",
            }}
          >
            {currentStep === "confirm" ? "Hoàn tất" : "Tiếp tục"}
          </button>
        </div>
      </div>
    </div>
  );
};
