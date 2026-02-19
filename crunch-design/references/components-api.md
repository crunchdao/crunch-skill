# @crunch-ui/core — Component API Reference

All components import from `@crunch-ui/core`. Built on Radix UI primitives + shadcn/ui patterns.

## Layout & Containers

### Card
`Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`
- `Card` accepts `displayCorners?: boolean`

### ScrollArea / ScrollBar
Radix scroll area with styled scrollbar.

### Sheet (Side Panel)
`Sheet`, `SheetTrigger`, `SheetClose`, `SheetContent`, `SheetHeader`, `SheetFooter`, `SheetTitle`, `SheetDescription`
- `SheetContent` accepts `side?: "top" | "right" | "bottom" | "left"`

## Overlays

### Dialog
`Dialog`, `DialogTrigger`, `DialogPortal`, `DialogClose`, `DialogOverlay`, `DialogContent`, `DialogHeader`, `DialogFooter`, `DialogTitle`, `DialogDescription`

### AlertDialog
`AlertDialog`, `AlertDialogTrigger`, `AlertDialogPortal`, `AlertDialogOverlay`, `AlertDialogContent`, `AlertDialogHeader`, `AlertDialogFooter`, `AlertDialogTitle`, `AlertDialogDescription`, `AlertDialogAction`, `AlertDialogCancel`

### Drawer (vaul)
`Drawer`, `DrawerTrigger`, `DrawerPortal`, `DrawerClose`, `DrawerOverlay`, `DrawerContent`, `DrawerHeader`, `DrawerFooter`, `DrawerTitle`, `DrawerDescription`

### Popover
`Popover`, `PopoverTrigger`, `PopoverAnchor`, `PopoverContent`
- `PopoverContent` accepts `matchTriggerWidth?: boolean`

### Tooltip
`TooltipProvider`, `Tooltip`, `TooltipTrigger`, `TooltipContent`

### Toast
`ToastProvider`, `ToastViewport`, `Toast`, `ToastAction`, `ToastClose`, `ToastTitle`, `ToastDescription`, `Toaster`
- `Toast` variant: `"default" | "destructive"`
- Use `useToast()` hook → `toast({ title, description, variant, action })`

## Actions

### Button
```ts
variant?: "primary" | "secondary" | "destructive" | "success" | "warning" | "outline" | "ghost"
size?: "default" | "sm" | "lg" | "icon" | "icon-sm" | "icon-lg"
loading?: boolean
asChild?: boolean
```
Also exports `buttonVariants` for use with `cn()`.

### Toggle
`Toggle` with `toggleVariants`. Variant: `"default" | "outline"`. Size: `"default" | "sm" | "lg"`.

### ToggleGroup
`ToggleGroup`, `ToggleGroupItem` — single or multiple selection.

## Navigation

### Breadcrumb
`Breadcrumb`, `BreadcrumbList`, `BreadcrumbItem`, `BreadcrumbLink`, `BreadcrumbPage`, `BreadcrumbSeparator`, `BreadcrumbEllipsis`
- `BreadcrumbLink` accepts `asChild?: boolean`

### Tabs
`Tabs`, `TabsList`, `TabsTrigger`, `TabsContent`
- `TabsList` and `TabsTrigger` accept `size?: "default" | "sm"`

### DropdownMenu
`DropdownMenu`, `DropdownMenuTrigger`, `DropdownMenuContent`, `DropdownMenuGroup`, `DropdownMenuItem`, `DropdownMenuCheckboxItem`, `DropdownMenuRadioGroup`, `DropdownMenuRadioItem`, `DropdownMenuLabel`, `DropdownMenuSeparator`, `DropdownMenuShortcut`, `DropdownMenuSub`, `DropdownMenuSubTrigger`, `DropdownMenuSubContent`, `DropdownMenuPortal`
- `DropdownMenuItem` and `DropdownMenuSubTrigger` accept `inset?: boolean`

### Command (cmdk)
`Command`, `CommandDialog`, `CommandInput`, `CommandList`, `CommandEmpty`, `CommandGroup`, `CommandItem`, `CommandSeparator`, `CommandShortcut`

## Forms

### Input
```ts
clearable?: boolean
debounceDelay?: number
rightSlot?: ReactNode
error?: boolean
rightSlotClassName?: string
```

### InputPassword
Password input with show/hide toggle.

### InputOTP
`InputOTP`, `InputOTPGroup`, `InputOTPSlot`, `InputOTPSeparator`

### Textarea
Standard textarea with Crunch styling.

### Select
`Select`, `SelectGroup`, `SelectValue`, `SelectTrigger`, `SelectContent`, `SelectLabel`, `SelectItem`, `SelectSeparator`, `SelectScrollUpButton`, `SelectScrollDownButton`

### Combobox / MultiCombobox
```ts
// Single select with search
interface ComboboxProps {
  options: { value: string; label: string }[];
  value: string | undefined | null;
  onChange: (value: string) => void;
  searchPlaceholder?: string;
  width?: string; height?: string;
  className?: string;
  messages?: { noOptions?: string; selectOption?: string; search?: string };
}

// Multi select with search
interface MultiComboboxProps {
  options: { value: string; label: string }[];
  values: string[];
  onChange: (values: string[]) => void;
  // same optional props as Combobox
}
```

### Checkbox
Radix checkbox.

### RadioGroup
`RadioGroup`, `RadioGroupItem`

### Switch
Radix switch toggle.

### Slider
`Slider`, `SliderValue` — `SliderValue` renders the current value display.

### Label
Styled label, compatible with `FormLabel`.

### Form (react-hook-form integration)
`Form`, `FormField`, `FormItem`, `FormLabel`, `FormControl`, `FormDescription`, `FormMessage`, `useFormField`

## Data Display

### Table
`Table`, `TableHeader`, `TableBody`, `TableFooter`, `TableRow`, `TableHead`, `TableCell`, `TableCaption`

### Badge
```ts
variant?: "primary" | "secondary" | "destructive" | "success" | "warning" | "outline" | "inverted"
size?: "default" | "sm"
```
Also exports `badgeVariants`.

### Alert
`Alert`, `AlertTitle`, `AlertDescription`
```ts
variant?: "default" | "destructive" | "success" | "warning" | "info"
```

### Avatar
`Avatar`, `AvatarImage`, `AvatarFallback`

### Accordion
`Accordion`, `AccordionItem`, `AccordionTrigger`, `AccordionContent`

### Progress
Radix progress bar.

### Pagination
```ts
interface PaginationProps {
  pagination: { page: number; size: number; totalPages?: number; totalElements?: number };
  pageSizes?: number[];
  onPaginationChange: (pagination: { page: number; size: number }) => void;
  loading?: boolean;
  messages?: Partial<PaginationMessages>;
}
```

## Feedback

### Skeleton
`Skeleton` — animated placeholder div.

### Loader / Loader2
Two spinner/loader animation components.

### Spinner
Another spinner variant.

### PulseRing
```ts
<PulseRing active={true} className="text-primary" />
```

## Utilities

### Legals
```ts
interface LegalsProps {
  className?: string;
  legalLinks?: { label: string; href: string }[];
}
```

### cn (from @crunch-ui/utils)
```ts
import { cn } from "@crunch-ui/utils";
cn("base-class", conditional && "active", className)
```

### generateLink (from @crunch-ui/utils)
```ts
generateLink("/competitions/:id", { id: "abc" }, { tab: "leaderboard" })
// → "/competitions/abc?tab=leaderboard"
```

### EXTERNAL_LINKS (from @crunch-ui/utils)
Pre-defined URLs: `HUB_V2`, `WEBSITE`, `DISCORD`, `TWITTER`, `LINKEDIN`, `YOUTUBE`, `FORUM`, `PHANTOM`, `PYPI`, etc.
