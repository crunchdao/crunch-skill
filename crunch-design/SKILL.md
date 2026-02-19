---
name: crunch-design
description: Use when building UI with @crunch-ui components, icons, or design tokens. Use when styling CrunchDAO apps, choosing colors, typography, or layout patterns. Use when importing from @crunch-ui/core, @crunch-ui/icons, @crunch-ui/utils, or @crunch-ui/tailwind-config.
---

# Crunch Design System

The `@crunch-ui` package family provides a shadcn/ui-based component library, icon set, design tokens, and Tailwind config for CrunchDAO applications.

## Packages

| Package | Purpose |
|---------|---------|
| `@crunch-ui/core` | UI components (Button, Dialog, Table, etc.) |
| `@crunch-ui/icons` | 261 SVG icon components |
| `@crunch-ui/utils` | `cn()` helper, color palette, external links |
| `@crunch-ui/tailwind-config` | Shared Tailwind config with typography, tokens, colors |

## Quick Start — New App Setup

```ts
// tailwind.config.ts
import sharedConfig from "@crunch-ui/tailwind-config";
import type { Config } from "tailwindcss";
import tailwindcssAnimate from "tailwindcss-animate";

const config: Pick<Config, "content" | "presets"> = {
  content: [
    "./src/**/*.{ts,tsx}",
    "./node_modules/@crunch-ui/core/**/*.{js,ts,jsx,tsx}",
  ],
  presets: [{
    ...sharedConfig,
    plugins: [...(sharedConfig.plugins ?? []), tailwindcssAnimate],
  }],
};
export default config;
```

```css
/* globals.css — required CSS variables (dark theme) */
@import "tailwindcss";
@config "../../tailwind.config.ts";

@theme inline {
  --font-departure: "departure", sans-serif;
  --background: 0 0% 19%;
  --foreground: 0 0% 98%;
  --muted: 0 0% 40%;
  --muted-foreground: 0 0% 74%;
  --card: 0 0% 11%;
  --card-foreground: 0 0% 98%;
  --popover: 0 0% 11%;
  --popover-foreground: 0 0% 98%;
  --border: 0 0% 32%;
  --input: 0 0% 11%;
  --input-foreground: 0 0% 98%;
  --primary: 21 83% 53%;
  --primary-accent: 21 83% 53;
  --primary-foreground: 0 0% 98%;
  --secondary: 0 0% 27%;
  --secondary-accent: 0 0% 27%;
  --secondary-foreground: 0 0% 98%;
  --secondary-inverted: 0 0% 86%;
  --accent: 0 0% 27%;
  --accent-foreground: 0 0% 98%;
  --destructive: 0 84% 60%;
  --destructive-accent: 0 84% 60%;
  --destructive-foreground: 0 0% 98%;
  --success: 146 85% 35%;
  --success-foreground: 0 0% 98%;
  --warning: 17 80% 48%;
  --warning-foreground: 0 0% 98%;
  --ring: 21 83% 53%;
}

@layer base {
  * { @apply border-border; }
  body { @apply bg-background text-foreground font-geist; }
}
```

## Component Usage

All components import from `@crunch-ui/core`:

```tsx
import { Button, Card, CardHeader, CardContent, Badge, Dialog, DialogContent, DialogTrigger } from "@crunch-ui/core";
import { cn } from "@crunch-ui/utils";
```

### Button Variants & Sizes

| Variant | Use for |
|---------|---------|
| `primary` | Main CTAs (orange) |
| `secondary` | Secondary actions (gray) |
| `destructive` | Delete, danger actions (red) |
| `success` | Confirm, positive actions (green) |
| `warning` | Caution actions (orange-dark) |
| `outline` | Bordered, transparent bg |
| `ghost` | No border, minimal emphasis |

| Size | Value |
|------|-------|
| `sm` / `icon-sm` | Small |
| `default` / `icon` | Medium |
| `lg` / `icon-lg` | Large |

```tsx
<Button variant="primary" size="sm" loading={isSubmitting}>Submit</Button>
<Button variant="ghost" size="icon"><SvgSettings /></Button>
```

### Badge Variants

Variants: `primary`, `secondary`, `destructive`, `success`, `warning`, `outline`, `inverted`. Sizes: `default`, `sm`.

### Alert Variants

Variants: `default`, `destructive`, `success`, `warning`, `info`.

## Typography Utilities

Two font families: **Geist** (body text) and **Departure** (titles, labels — uppercase display font).

| Class | Font | Size | Line Height |
|-------|------|------|-------------|
| `display-xl` | Geist | 96px | 120px |
| `display-lg` | Geist | 64px | 80px |
| `display` | Geist | 48px | 64px |
| `display-sm` | Geist | 32px | 40px |
| `title-lg` | Departure ↑ | 24→32px | 40px |
| `title` | Departure ↑ | 24px | 32px |
| `title-sm` | Departure | 18px | 24px |
| `title-xs` | Departure | 14px | 18px |
| `title-2xs` | Departure | 12px | 16px |
| `body-xl` | Geist | 32px | 40px |
| `body-lg` | Geist | 24px | 32px |
| `body` | Geist | 18px | 24px |
| `body-sm` | Geist | 14px | 18px |
| `body-xs` | Geist | 12px | 16px |
| `label-lg` | Departure | 18px | 24px |
| `label` | Departure | 16px | 20px |
| `label-sm` | Departure | 14px | 18px |
| `label-xs` | Departure | 12px | 16px |
| `label-2xs` | Departure | 11px | 14px |

↑ = uppercase by default

## Icons

261 icons from `@crunch-ui/icons`, all named `Svg<PascalCase>`:

```tsx
import { SvgRocket, SvgSettings, SvgTrash, SvgCheck } from "@crunch-ui/icons";
<SvgRocket className="size-4" />
```

Full icon list: [references/icons.md](references/icons.md)

## Color System

### Semantic Colors (CSS variables, used via Tailwind)

Use these for UI elements — they reference CSS variables and adapt to theming:

`bg-background`, `text-foreground`, `bg-card`, `bg-muted`, `text-muted-foreground`, `bg-primary`, `text-primary-foreground`, `bg-destructive`, `bg-success`, `bg-warning`, `border-border`, `bg-input`, `ring-ring`

### Raw Palette (from `@crunch-ui/utils` theme)

For data visualization, charts, or non-semantic use. Available as Tailwind classes (e.g. `text-orange-500`, `bg-neutral-900`):

Palettes: `gray`, `neutral`, `bone`, `red`, `orange`, `yellow`, `lime`, `green`, `teal`, `blue`, `violet`, `pink`, `sky` — each with shades 50–950.

Full palette values: [references/color-palette.md](references/color-palette.md)

## Special Utilities

| Class | Effect |
|-------|--------|
| `primary-animated-border` | Animated conic-gradient border (orange) |
| `destructive-animated-border` | Animated border (red) |
| `success-animated-border` | Animated border (green) |
| `custom-scrollbar` | Styled 6px scrollbar matching border color |
| `no-scrollbar` | Completely hidden scrollbar |

## Common Patterns

### Form with validation
```tsx
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage, Input, Button } from "@crunch-ui/core";
import { useForm } from "react-hook-form";
```

### Combobox (searchable select)
```tsx
import { Combobox, MultiCombobox } from "@crunch-ui/core";
<Combobox options={[{value: "a", label: "A"}]} value={val} onChange={setVal} />
```

### Toast notifications
```tsx
import { useToast, Toaster } from "@crunch-ui/core";
const { toast } = useToast();
toast({ title: "Success", variant: "default" });
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using raw colors for semantic UI | Use `bg-primary`, `text-destructive`, etc. |
| Importing shadcn directly | Import from `@crunch-ui/core` instead |
| Missing `tailwindcss-animate` plugin | Add to tailwind config plugins array |
| Missing CSS variables in globals.css | Copy the `@theme inline` block above |
| Using `font-sans` | Use `font-geist` (body) or `font-departure` (titles) |
| Writing custom typography classes | Use built-in utilities: `title`, `body-sm`, `label`, etc. |

## Reference

- Component API (full type definitions): [references/components-api.md](references/components-api.md)
- Icon list: [references/icons.md](references/icons.md)
- Color palette values: [references/color-palette.md](references/color-palette.md)
