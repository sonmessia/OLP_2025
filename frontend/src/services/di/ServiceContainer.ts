import type { ISensorRepository } from "../../domain/repositories/ISensorRepository";
import { GetAllSensorsUseCase } from "../../domain/use-cases/GetAllSensorsUseCase";
import { GetSensorByIdUseCase } from "../../domain/use-cases/GetSensorByIdUseCase";
import { RefreshSensorsUseCase } from "../../domain/use-cases/RefreshSensorsUseCase";
import { MockSensorRepository } from "../repositories/MockSensorRepository";

export class ServiceContainer {
  private static instance: ServiceContainer;

  private _sensorRepository: ISensorRepository;

  private constructor() {
    // Initialize repositories
    this._sensorRepository = new MockSensorRepository();
  }

  static getInstance(): ServiceContainer {
    if (!ServiceContainer.instance) {
      ServiceContainer.instance = new ServiceContainer();
    }
    return ServiceContainer.instance;
  }

  // Repository getters
  get sensorRepository(): ISensorRepository {
    return this._sensorRepository;
  }

  // Use case factories
  createGetAllSensorsUseCase(): GetAllSensorsUseCase {
    return new GetAllSensorsUseCase(this._sensorRepository);
  }

  createGetSensorByIdUseCase(): GetSensorByIdUseCase {
    return new GetSensorByIdUseCase(this._sensorRepository);
  }

  createRefreshSensorsUseCase(): RefreshSensorsUseCase {
    return new RefreshSensorsUseCase(this._sensorRepository);
  }
}
