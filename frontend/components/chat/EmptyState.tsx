// frontend/components/chat/EmptyState.tsx

import React from 'react';

export const EmptyState: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full p-4 text-center">
      <h2 className="text-xl font-semibold">Start a new conversation</h2>
      <p className="text-gray-500">
        You can ask the AI to help you manage your todos. For example: &quot;Add a new task to buy milk&quot;.
      </p>
    </div>
  );
};
