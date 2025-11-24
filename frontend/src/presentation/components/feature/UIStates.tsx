import React from "react";

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  text?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = "md",
  text,
}) => {
  const sizeClasses = {
    sm: "w-4 h-4 border-2",
    md: "w-8 h-8 border-2",
    lg: "w-12 h-12 border-3",
  };

  return (
    <div className="flex flex-col items-center justify-center gap-3 py-8">
      <div
        className={`spinner ${sizeClasses[size]}`}
        style={{
          borderColor: "var(--color-border)",
          borderTopColor: "var(--color-primary)",
        }}
      />
      {text && (
        <p
          className="text-sm font-medium"
          style={{ color: "var(--color-text-secondary)" }}
        >
          {text}
        </p>
      )}
    </div>
  );
};

interface EmptyStateProps {
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  description,
  action,
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      <div
        className="text-6xl mb-4"
        style={{ color: "var(--color-text-tertiary)" }}
      >
        📊
      </div>
      <h3
        className="text-lg font-semibold mb-2"
        style={{ color: "var(--color-text-primary)" }}
      >
        {title}
      </h3>
      {description && (
        <p
          className="text-sm text-center max-w-md mb-4"
          style={{ color: "var(--color-text-secondary)" }}
        >
          {description}
        </p>
      )}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
};

interface ErrorStateProps {
  title: string;
  message?: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title,
  message,
  onRetry,
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      <div className="text-6xl mb-4" style={{ color: "var(--color-error)" }}>
        ⚠️
      </div>
      <h3
        className="text-lg font-semibold mb-2"
        style={{ color: "var(--color-text-primary)" }}
      >
        {title}
      </h3>
      {message && (
        <p
          className="text-sm text-center max-w-md mb-4"
          style={{ color: "var(--color-text-secondary)" }}
        >
          {message}
        </p>
      )}
      {onRetry && (
        <button className="btn btn-primary mt-4" onClick={onRetry}>
          Thử lại
        </button>
      )}
    </div>
  );
};
