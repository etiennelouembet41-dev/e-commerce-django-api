import {
  CheckCircle,
  Circle,
} from "lucide-react";

export default function ImportTimeline({ timeline = [] }) {
  return (
    <div className="space-y-6">
      {timeline.map((step, index) => (
        <div key={step.status} className="flex gap-4">
          <div className="flex flex-col items-center">
            {step.completed ? (
              <CheckCircle className="text-green-500" />
            ) : (
              <Circle className="text-gray-500" />
            )}

            {index !== timeline.length - 1 && (
              <div className="mt-2 h-10 w-[2px] bg-white/10" />
            )}
          </div>

          <div>
            <h3
              className={
                step.current
                  ? "font-bold text-red-500"
                  : "font-semibold text-white"
              }
            >
              {step.status}
            </h3>

            {step.current && (
              <p className="text-sm text-gray-400">
                Étape actuelle
              </p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}