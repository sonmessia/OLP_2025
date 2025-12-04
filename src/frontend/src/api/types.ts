export interface NgsiLdAttributePatch {
  type: "Property" | "Relationship" | "GeoProperty" | "VocabProperty";
  value?: unknown;
  object?: string;
  observedAt?: string;
  unitCode?: string;
}

export interface BatchOperationRequest<T> {
  entities: T[];
}

export interface BatchDeleteRequest {
  entity_ids: string[];
}

export interface QueryParams {
  id?: string;
  q?: string;
  pick?: string;
  attrs?: string;
  georel?: string;
  geometry?: string;
  coordinates?: string;
  geoproperty?: string;
  limit?: number;
  offset?: number;
  count?: boolean;
  format?: string;
  options?: string;
  local?: boolean;
  tenant?: string;
  entity_type?: string;
}

export interface EntityInfo {
  type?: string;
  id?: string;
}

export interface ManagementInfo {
  interval?: number;
  timeout?: number;
}

export interface RegistrationCreate {
  description: string;
  entities: EntityInfo[];
  endpoint: string;
  mode: "inclusive" | "redirect" | "exclusive" | "auxiliary";
  operations?: string[];
  propertyNames?: string[];
  relationshipNames?: string[];
  expiresAt?: string;
  management?: ManagementInfo;
  contextSourceInfo?: Record<string, string>[];
}

export interface RegistrationUpdate {
  description?: string;
  endpoint?: string;
  expiresAt?: string;
  management?: ManagementInfo;
  contextSourceInfo?: Record<string, string>[];
}

export interface ContextSourceRegistration extends RegistrationCreate {
  id: string;
  type: string;
  createdAt?: string;
  modifiedAt?: string;
  status?: string;
}
